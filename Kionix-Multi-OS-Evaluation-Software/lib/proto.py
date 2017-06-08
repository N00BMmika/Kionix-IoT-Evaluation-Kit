# 
# Copyright 2016 Kionix Inc.
#
try:
    import serial
except ImportError:
    print '\nPySerial not installed. Please run: pip install pyserial==3.0.1\n'
    raise

assert serial.VERSION.startswith('3.'),'pyserial 3.x required. Please run: pip install pyserial==3.0.1'

import subprocess, os, time, socket, signal

#
# definitions for kionix evaluation kit protocol
# 
EVKIT_ERROR_BASE_NUM                                    = 0x00

# Status code
EVKIT_SUCCESS                                           = (EVKIT_ERROR_BASE_NUM + 0)  
EVKIT_BUS1_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 1)  
EVKIT_BUS2_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 2)  
EVKIT_GPIO_INVALID                                      = (EVKIT_ERROR_BASE_NUM + 3)  
EVKIT_GPIO_RESERVED                                     = (EVKIT_ERROR_BASE_NUM + 4)  
EVKIT_MAX_GPIO_RESERVED                                 = (EVKIT_ERROR_BASE_NUM + 5)  
EVKIT_MAX_EXE_PARAMS_ERROR                              = (EVKIT_ERROR_BASE_NUM + 6)
EVKIT_INTERRUPT_WAITING                                 = (EVKIT_ERROR_BASE_NUM + 7)  
EVKIT_INTERRUPT_DETECTED                                = (EVKIT_ERROR_BASE_NUM + 8)  
EVKIT_DATA_READ_ERROR                                   = (EVKIT_ERROR_BASE_NUM + 9)  
EVKIT_DATA_STREAM_ACTIVE                                = (EVKIT_ERROR_BASE_NUM + 10)
EVKIT_GPIO_STATUS_READ_ERROR                            = (EVKIT_ERROR_BASE_NUM + 11)
EVKIT_MSG_LENGHT_ERROR                                  = (EVKIT_ERROR_BASE_NUM + 12)
EVKIT_BUS2_BUFFER_FULL                                  = (EVKIT_ERROR_BASE_NUM + 13)
EVKIT_INVALID_MESSAGE                                   = (EVKIT_ERROR_BASE_NUM + 14)
EVKIT_INVALID_STATE                                     = (EVKIT_ERROR_BASE_NUM + 15)

# constants
EVKIT_PROTOCOL_VERSION_MAJOR                            = 0x01
EVKIT_PROTOCOL_VERSION_MINOR                            = 0x01

EVKIT_MSG_MAX_PAYLOAD_SIZE                              = 0x0c # size in bytes 12
EVKIT_MSG_MAX_PAYLOAD_IND_SIZE                          = 0x12 # size in bytes 18
EVKIT_MSG_MAX_EXE_PARAMS                                = 0x04
EVKIT_MSG_MAX_GPIO                                      = 0x04

EVKIT_MSG_HEADER_LENGH                                  = 0x02
EVKIT_MSG_BUS_PARAMS_LENGH                              = 0x02

EVKIT_MSG_GPIO_PIN_NOSENSE                              = 0x00
EVKIT_MSG_GPIO_PIN_SENSE_LOW                            = 0x01
EVKIT_MSG_GPIO_PIN_SENSE_HIGH                           = 0x02  

EVKIT_MSG_GPIO_PIN_NOPULL                               = 0x00
EVKIT_MSG_GPIO_PIN_PULLDOWN                             = 0x01
EVKIT_MSG_GPIO_PIN_PULLUP                               = 0x02

EVKIT_GPIO_PIN_NOSENSE                                  = 0x00
EVKIT_GPIO_PIN_SENSE_LOW                                = 0x01
EVKIT_GPIO_PIN_SENSE_HIGH                               = 0x02  

EVKIT_GPIO_PIN_NOPULL                                   = 0x00
EVKIT_GPIO_PIN_PULLDOWN                                 = 0x01
EVKIT_GPIO_PIN_PULLUP                                   = 0x02

EVKIT_RESET_SOFT                                        = 0x00
EVKIT_RESET_HARD                                        = 0x01

# protocol messages
EVKIT_MSG_READ_REQ                                      = 0x01
EVKIT_MSG_READ_RESP                                     = 0x02

EVKIT_MSG_WRITE_REQ                                     = 0x03
EVKIT_MSG_WRITE_RESP                                    = 0x04

EVKIT_MSG_VERSION_REQ                                   = 0x05
EVKIT_MSG_VERSION_RESP                                  = 0x06

EVKIT_MSG_ENABLE_INT_REQ                                = 0x07
EVKIT_MSG_ENABLE_INT_RESP                               = 0x08

EVKIT_MSG_DISABLE_INT_REQ                               = 0x09
EVKIT_MSG_DISABLE_INT_RESP                              = 0x10

EVKIT_MSG_GPIO_STATE_REQ                                = 0x0E
EVKIT_MSG_GPIO_STATE_RESP                               = 0x0F

EVKIT_MSG_ERROR_IND                                     = 0x11
EVKIT_MSG_RESET_REQ                                     = 0x12 # no response sent from this req

EVKIT_MSG_INTERRUPT_IND1                                = 0x0A
EVKIT_MSG_INTERRUPT_IND2                                = 0x0B
EVKIT_MSG_INTERRUPT_IND3                                = 0x0C
EVKIT_MSG_INTERRUPT_IND4                                = 0x0D

class ProtocolException(Exception): pass
class ProtocolTimeoutException(ProtocolException): pass
class ProtocolBus1Exception(ProtocolException): pass

class kx_socket_port(object):
    def __init__(self, host = 'localhost', port = 8100, timeout = 3):
        self._start_child_process(port)
        self.timeout = timeout
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(self.timeout)
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

        for i in range(10):
            try:
                self.conn.connect((host, port))
            except socket.timeout:                                
                self.conn.close()
                self.conn = None
                if (i == 9):                    
                    raise ProtocolException('Socket opening failed - timeout')
            except socket.error, err:                 
                self.conn.close()
                self.conn = None            
                if (i == 9):                    
                    raise ProtocolException('Socket opening failed')
                else:
                    time.sleep(0.5)
            else:
                break

            # create socket again with longer timeout
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # NOTE: When error "[Errno 10061] No connection could be made because the target machine actively refused it" comes, timeout does not seem to matter
            self.conn.settimeout(self.timeout)
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

    def flush(self):
        # use short time out and read all data available in socket
        counter = 100
        self.conn.settimeout(0.01)
        while self.conn.recv():
            time.sleep(0.01)
            counter -=1
            if counter == 0:
                raise ProtocolException('Socket flushing unsuccessful.')
            pass
        
        # restore original timeout setting
        self.conn.settimeout(self.timeout)
        
    def close(self):
        self.conn.close()
        self._stop_child_process()
        self.conn = None

    def write(self, data):
        self.conn.sendall(data)

    def read(self, length):
        self.conn.settimeout(self.timeout)
        return self.conn.recv(length)
        
    def _start_child_process(self, port):
        assert 0, "To be implemented in the class which is deriving this class."
    def _stop_child_process(self):
        assert 0, "To be implemented in the class which is deriving this class."

        
class kx_socket_adb(kx_socket_port):
    DEVICE_SOCKET_PORT = 8123
    LOCAL_SOCKET_PORT = 8100
    def _start_child_process(self, port):
        self.LOCAL_SOCKET_PORT = port
        thispath, thisfile = os.path.split(__file__)
        self.ADB_PATH = os.path.join(thispath, 'adb.exe')
        if os.path.isfile(self.ADB_PATH):
            pass
            #logger.debug('ADB.EXE found from lib/ directory')
        else:
            #logger.debug('ADB.EXE NOT found from lib/ directory')
            self.ADB_PATH = 'adb.exe'
        try:
            subprocess.call('%s forward --remove-all' % self.ADB_PATH)
        except WindowsError:
            raise ProtocolException('ADB.EXE not found. Please download adb and add the location of adb.exe to PATH environment variable or copy adb.exe (and relate DLLs) under lib/ directory.')

        subprocess.call('%s forward tcp:%s tcp:%s' % (self.ADB_PATH, self.LOCAL_SOCKET_PORT, self.DEVICE_SOCKET_PORT))

    def _stop_child_process(self):
        # remove port forwarding, ADB will stay on background. This is default way how adb works
        subprocess.call('%s forward --remove-all' % self.ADB_PATH)

class kx_socket_b2s(kx_socket_port):
    def _start_child_process(self, port):       
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        thispath, thisfile = os.path.split(__file__)
        B2S_path = os.path.join(thispath, 'B2S.exe')
        if os.path.isfile(B2S_path):
            #https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx
            #CREATE_NEW_PROCESS_GROUP=0x00000200 -> If this flag is specified, CTRL+C signals will be disabled            
            self._p = subprocess.Popen(B2S_path + ' -p %s' % port, startupinfo=startupinfo, creationflags=0x00000200, stdout=subprocess.PIPE) # pipe stdout to see only errors in console
            time.sleep(1)
            pass
        else:
            raise ProtocolException('B2S.exe not found.')

    def close(self):
        self.write(reset_req())
        self.conn.close()
        self._stop_child_process()
        self.conn = None

    def _stop_child_process(self):
        #self._p.kill()

        # NOTE: Must use CTLR + BREAK event instead of CTRL + C, which has been disabled
        os.kill(self._p.pid, signal.CTRL_BREAK_EVENT)         

class kx_com_port(object):
    def __init__(self, comport, baudrate, timeout):
        self._com = serial.Serial(port=comport, baudrate=baudrate, timeout=timeout)

    def read(self, length = 1):
        data = self._com.read(length)
        if data is None or data == '':
            raise ProtocolException('COM port reading failure')

        return data

    def flush(self):
        while self._com.in_waiting:
            self._com.read()
        
    def write(self, data):
        self._com.write(data)

    def close(self):
        self._com.close()
                
class ProtocolEngine(object):
    def __init__(self, connection):
        self.connection = connection
        self.message_fifo = []
        
    def send_message(self, data):
        self.connection.write(data)
            
    def get_message_type(self, message):
        return ord(message[1])

    def get_stream_id(self, message):
        message_type = self.get_message_type(message)
        if message_type != EVKIT_MSG_ENABLE_INT_RESP:
            raise ProtocolException('Invalid message type %d' % message_type) 

        return ord(message[2])            

    def receive_message(self, waif_for_message = None):
        retry_count = 200

        # check if wanted message already received and can be found from FIFO
        if len(self.message_fifo) > 0:
            for fifo_index in range(len(self.message_fifo)):
                received_message = self.message_fifo[fifo_index]
                
                if waif_for_message == None or \
                   self.get_message_type(received_message) == waif_for_message:
                    self.message_fifo.pop(fifo_index) # remove this message from fifo
                    return received_message

            # continue to receive new messages if wanted message was not in FIFO
            
        while (retry_count):
            received_message = self._receive_single_message()
            if waif_for_message == None or \
               self.get_message_type(received_message) == waif_for_message:
                return received_message
            else:
                self.message_fifo.append(received_message)
                retry_count-=1

        raise ProtocolException('Message FIFO full')
        
    def _receive_single_message(self):
        received_message = ''
        partial_message = ''
        retry_count = 2
        length_byte = self.connection.read(1)
        if length_byte == '' or length_byte is None:
            raise ProtocolTimeoutException('Timeout on message receiving 1.')

        #received_message = data

        message_length = ord(length_byte) - 1 # -1 since length takes 1 byte
        while (retry_count):
            partial_message = self.connection.read(message_length - len(partial_message))
            retry_count -= 1
            received_message += partial_message
            if len (partial_message) == message_length:
                assert len(received_message) > 1
                return length_byte+received_message

        raise ProtocolTimeoutException('Timeout on message receiving 2.')

class message_container:
    def __init__(self, message_type, max_len = 20):
        self.message_type = message_type
        self.len = 2
        self.payload = ''
        self.max_len = max_len

    def append_payload(self, data):
        "accepts int8 or string linght of 1 or more"
        if isinstance(data, int):
            self.payload += chr(data)
            self.len += 1
            
        elif isinstance(data, str):
            self.payload += data
            self.len += len(data)

        elif isinstance(data, list):
            for t in data:
                if isinstance(t, int):
                    self.payload += chr(t)
                    self.len += 1
                    
                elif isinstance(t, str):
                    self.payload += t
                    self.len += len(t)
        else:
            raise ProtocolException('Invalid value for message payload')
        
    def get_message(self):
        message = '%c%c%s' % (self.len, self.message_type, self.payload)
        if len(message) > self.max_len:
            raise ProtocolException('Message too long')

        return message


#
# request message packing
#

def reset_req(reset_type = EVKIT_RESET_SOFT):
    assert reset_type in [EVKIT_RESET_SOFT, EVKIT_RESET_HARD]
    msg = message_container(EVKIT_MSG_RESET_REQ)
    msg.append_payload(reset_type)
    return msg.get_message()
    
def write_req(sad, register, value):
    msg = message_container(EVKIT_MSG_WRITE_REQ)
    msg.append_payload(sad)
    msg.append_payload(register)
    msg.append_payload(value)
    return msg.get_message()

def read_req(sad, register, length=1):
    msg = message_container(EVKIT_MSG_READ_REQ)
    msg.append_payload([sad,register,length])
    return msg.get_message()

def version_req():
    msg = message_container(EVKIT_MSG_VERSION_REQ)
    return msg.get_message()

def gpio_state_req(gpio_nrb):
    msg = message_container(EVKIT_MSG_GPIO_STATE_REQ)
    msg.append_payload(gpio_nrb)
    return msg.get_message()

def interrupt_disable_req(pin,
                          sense = EVKIT_GPIO_PIN_SENSE_LOW,
                          pull = EVKIT_GPIO_PIN_PULLUP):
    
    msg = message_container(EVKIT_MSG_DISABLE_INT_REQ)
    msg.append_payload(pin)
    msg.append_payload(sense)
    msg.append_payload(pull)
    return msg.get_message()
    
def interrupt_enable_req(pin, payload_definition,
                         sense = EVKIT_GPIO_PIN_SENSE_LOW,
                         pull = EVKIT_GPIO_PIN_PULLUP
                         ):
    msg = message_container(EVKIT_MSG_ENABLE_INT_REQ)
    msg.append_payload(pin)
    msg.append_payload(sense)
    msg.append_payload(pull)
    msg.append_payload(payload_definition)
    if len(payload_definition) % 3 != 0:
        raise ProtocolException('payload definition must be in format (sad,reg,len)*n')
    return msg.get_message()

#
# message unpacking
#
def _check_response_status(message_status):
    if message_status == EVKIT_BUS1_ERROR:
        raise ProtocolBus1Exception()

    if message_status != EVKIT_SUCCESS:
        #print 'Error message received %d' % message_status
        raise ProtocolException('Error message received %d' % message_status)
    
def unpack_response_data(message):
    # convert string to list of int8
    message = [ord(t) for t in message]
    message_type = message[1]

    if message_type in [EVKIT_MSG_READ_RESP, EVKIT_MSG_WRITE_RESP]:
        message_sad = message[2]
        message_register = message[3]
        message_status = message[4]
        _check_response_status(message_status)

        if message_type == EVKIT_MSG_READ_RESP:
            message_payload = message[5:]
            return message_type, message_payload
        
    elif message_type in [EVKIT_MSG_VERSION_RESP]:
        message_status = message[2]
        _check_response_status(message_status)

        message_major_version = message[3]
        message_minor_version = message[4]
        return message_type, message_major_version, message_minor_version

    elif message_type in [EVKIT_MSG_ENABLE_INT_RESP]:
        message_stream_id = message[2]
        message_status = message[3]
        _check_response_status(message_status)
        return message_type, message_stream_id

    elif message_type in [EVKIT_MSG_DISABLE_INT_RESP]:
        message_status = message[2]
        _check_response_status(message_status)

    elif message_type in [EVKIT_MSG_GPIO_STATE_RESP]:
        message_stream_gpio_ind = message[2]
        message_stream_gpio_state = message[3]
        message_status = message[4]
        _check_response_status(message_status)
        if message_stream_gpio_state == EVKIT_MSG_GPIO_PIN_SENSE_HIGH:
            gpio_state = 1
        else:
            gpio_state = 0
            
        return message_type, gpio_state

    elif message_type in [EVKIT_MSG_INTERRUPT_IND1,
                          EVKIT_MSG_INTERRUPT_IND2,
                          EVKIT_MSG_INTERRUPT_IND3,
                          EVKIT_MSG_INTERRUPT_IND4]:
        
        message_payload = message[1:]
        return message_type, message_payload
        
    elif message_type in [EVKIT_MSG_ERROR_IND]:
        message_status = message[2]
        raise ProtocolException('Unspefied event occured %d' % message_status)
        #return message_type, message_status

    else:
        raise ProtocolException('Unknown message received 0x%02x' % message_type)
        
    return message_type 
