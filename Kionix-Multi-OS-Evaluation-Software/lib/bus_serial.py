# 
# Copyright 2016 Kionix Inc.
#
from bus_base import _i2c_bus, BusException
from bus_base import _i2c_bus, BusException
from evkit_protocol import evkit_handle_protcol_msg, ProtocolException
from util_lib import logger, DelayedKeyboardInterrupt, evkit_config
from time import sleep
from struct import unpack
import array

try:
    import serial
except ImportError:
    print '\nPySerial not installed. Please run pip install pyserial==3.0.1\n'
    raise

assert serial.VERSION.startswith('3.'),'pyserial 3.x required. Please run: pip install pyserial==3.0'


class bus_serial_com(_i2c_bus):
    # TODO demonstarte how to put sensor to hs mode
    def __init__(self, index = None ):
        # FIXME consider removing index
        _i2c_bus.__init__(self)
        #self._handle = None
        self._ser = None
        self.bus_gpio_list = []
        self._has_gpio = False
        self._gpio_pin_index = []
        
        self.config_section = evkit_config.get('__com__','config')
        
        # Add protocol msg set iopin config
        self._message_handler = evkit_handle_protcol_msg()
        self._configure_interrupts()

    def _configure_interrupts(self):
        # add all defined GPIO pins
        self.bus_gpio_list = []
        self._gpio_pin_index = []
        for t in range(1,4):
            if not evkit_config.has_option(self.config_section,'pin%d_index' % t):
                break
            self._has_gpio = True
            self.bus_gpio_list.append(t)
            self._gpio_pin_index.append(evkit_config.getint(self.config_section,'pin%d_index' % t))
    
    def configure(self, cfg):
        pass

    def get_configuration_template(self):
        return {}

    def recv_msg(self, ThrowExceptionIfTimeout = True):
        # Read message length and unpack it into an integer
        retry = 2
        while(retry):
            raw_msglen = self._ser.read(1)
            if  len(raw_msglen)>0:
        
                msglen = unpack('<b', raw_msglen)[0]
                msglen = msglen - 1
                # Read the message data
                #TODO: add len validation check
                return self.recvall(msglen)
            logger.debug('Serial read timeout. Retry.')

            retry-=1

        if ThrowExceptionIfTimeout:
            config_section = evkit_config.get('__com__','config')
            # FIXME if autoconnection is used, this prints "no response from auto"
            raise ProtocolException('No response from %s.' % evkit_config.get(config_section, 'com_port'))

        # here when no data and ThrowExceptionIfTimeout is False
        return None

    def recvall(self,n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = self._ser.read(n - len(data))
            if not packet:
                logger.debug('Protocol problem')
                return None
            data += packet
        return data

    def close(self):
        self._ser.close()

    def _flush_input(self):
        # flush input, there may be some old data in buffer
        flushed = False
        while self._ser.in_waiting:
            self._ser.read()
            flushed = True

        if flushed:
            logger.debug('Flushing serial input.')

    def get_com_port(self):
        try:
            import wmi
        except ImportError:
            print "\nPlease run \'pip install wmi\'\nand \'pip install pypiwin32\'\n"
            raise
       
        c = wmi.WMI()
        
        # query based on configured device
        if self.config_section == 'serial_com_kx_iot':
            wql = "SELECT * FROM Win32_PnPEntity WHERE Description = 'USB Serial Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'"
        else:
            wql = "SELECT * FROM Win32_PnPEntity WHERE Description = 'Arduino Uno' AND NOT PNPDeviceID LIKE 'ROOT\\%'"

        result = None
        
        for foundPort in c.query(wql):
            result = foundPort.Name.partition('(')[2].partition(')')[0]

        if result == None:
            raise BusException('Automatic search found no devices')
        else:
            logger.info('Automatic port choice: %s', result)
            return result

    def open(self):
        config_section = evkit_config.get('__com__','config')

        if evkit_config.get(config_section, 'com_port').lower() == "auto":
            comport = self.get_com_port()
            
        else:    
            comport = evkit_config.get(config_section, 'com_port')
 
        baudrate = evkit_config.getint(config_section, 'baudrate')
        delay_s = evkit_config.getint(config_section, 'start_delay_s')
        self._ser = serial.Serial(comport,baudrate, timeout = 5)

        
        if delay_s>0:
            logger.info('Waiting %d seconds', delay_s)
            sleep(delay_s)
        
        request_data = self._message_handler.version_req()
        #self._ser.write(request_data)
        #self._flush_input()
        self._ser.write(request_data)
        reponse_data = self.recv_msg()
        
        if reponse_data is None:
            raise ProtocolException('No response from %s. Please check COM port number and baudrate.' % comport)

        #resp_string = map(hex,map(ord,data))
        #print "version resp data:"
        #print resp_string
        # Handle response message
        try:
            self._message_handler.handle_version_resp(reponse_data)
        except ProtocolException:
            # try another time
            logger.debug('Version query failed. Try 2nd time.')
            sleep(0.1)
            self._flush_input()
            sleep(0.1)
            self._ser.write(request_data)
            reponse_data = self.recv_msg()
            self._message_handler.handle_version_resp(reponse_data)
            
        _i2c_bus.open(self)

    def enable_interrupt(self, pin, payload_definition):
        data = self._message_handler.interrupt_enable_req(pin, payload_definition)
##        print '<start_msg>%s</start_msg>' % ','.join([str(ord(t)) for t in data])
        self._ser.write(data)

        # Read data using validation
        resp = self.recv_msg()
        
        #print 'enable int resp: ',map(hex,map(ord,resp))
        return self._message_handler.handle_interrupt_enable_resp(resp)

    def __enable_interrupt(self, pin, sensor, register, msglen):
        sad = self._sensortable[sensor]

        data = self._message_handler.interrupt_enable_req(pin, sad, register, msglen)
##        print '<start_msg>%s</start_msg>' % ','.join([str(ord(t)) for t in data])
        self._ser.write(data)

        # Read data using validation
        resp = self.recv_msg()
        #print 'enable int resp: ',map(hex,map(ord,resp))
        #data = self._message_handler.handle_interrupt_enable_resp(data,length)
        return resp
        
##    def enable_interrupt_9d(self, pin, params_array):
##        data = self._message_handler.interrupt_enable_req_9d(pin, params_array)
##        print '<start_msg>%s</start_msg>' % ','.join([str(ord(t)) for t in data])
##        self._ser.write(data)
##
##        # Read data using validation
##        resp = self.recv_msg()
##        print 'enable int resp: ',map(hex,map(ord,resp))
##        #data = self._message_handler.handle_interrupt_enable_resp(data,length)
        
    def disable_interrupt(self, pin):
        data = self._message_handler.interrupt_disable_req(pin)
        #print '<end_msg>%s</end_msg>' % ','.join([str(ord(t)) for t in data])
        self._ser.write(data)

        # Read data using validation
        resp = self.recv_msg()
        #print 'disable int resp: ',map(hex,map(ord,resp))
        #data = self._message_handler.handle_interrupt_disable_resp(data,length)
        return resp

    def wait_indication(self):
        resp = self.recv_msg(False)
        if resp is None: return resp
        
        arr=array.array('B')
        arr.fromstring(resp)
        return arr

    def read_register(self, sensor, register, length=1):
        sad = self._sensortable[sensor]
        retrycount = 0
        data = self._message_handler.read_req(sad,register,length)

        with DelayedKeyboardInterrupt():

            self._ser.write(data)
            # Read data using validation
            data = self.recv_msg()
            if data is None:
                logger.debug('bus_serial : retry read')
                data = self.recv_msg()
##            
##            while retrycount < 5 and data is None:
##                logger.debug('bus_serial : retry read')
##                data = self.recv_msg()
##                sleep(0.05)
##                retrycount += 1
        
        data = self._message_handler.handle_read_resp(data,length)
        arr=array.array('B')
        arr.fromstring(data)
        return arr
    
    def write_register(self, sensor, register, value):
        sad = self._sensortable[sensor]
        data = self._message_handler.write_req(sad,register,value)
        with DelayedKeyboardInterrupt():
            self._ser.write(data)
            # Read data using validation
            data = self.recv_msg()        

        self._message_handler.handle_write_resp(data) 

    def gpio_read(self, gpio):
        "Reads physical GPIO pin"
        #print 'gpio read',gpio
        data = self._message_handler.gpio_state_req(gpio)

        with DelayedKeyboardInterrupt():
            self._ser.write(data)
            # Read data using validation
            data = self.recv_msg()

        #print 'data', [hex(ord(t)) for t in data]
        sense = self._message_handler.handle_gpio_state_resp(data)
        #print 'sense',sense
        return sense
 
    def poll_gpio(self, index):
        "Polls logical GPIO pin"
        #print 'gpio poll',index
        assert index in self.bus_gpio_list
        return self.gpio_read(self._gpio_pin_index[index-1])
