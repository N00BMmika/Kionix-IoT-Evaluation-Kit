# 
# Copyright 2016 Kionix Inc.
#
from time import sleep
import array
import os

from bus_base import _i2c_bus, BusException
from util_lib import logger, DelayedKeyboardInterrupt, evkit_config
import proto
     
class kx_protocol_bus(_i2c_bus):
    def  __init__(self):
        _i2c_bus.__init__(self)
        self._gpio_pin_index = []
        self._kx_connection = None
        self._kx_port = None
        self.protocol_major_version = -1
        self.protocol_minor_version = -1
        
    def configure(self, cfg):
        pass

    def get_configuration_template(self):
        return {}

    def close(self):
        _i2c_bus.close(self)
        self._kx_port.close()

    def verify_protocol_version(self, major_version, minor_version):
        # check that FW has correct version

        self.protocol_major_version = major_version
        self.protocol_minor_version = minor_version

        if major_version != proto.EVKIT_PROTOCOL_VERSION_MAJOR or \
           minor_version != proto.EVKIT_PROTOCOL_VERSION_MINOR:
            # raise proto.ProtocolException('Wrong protocol version received from Firmware. Expected %d.%d, received %d.%d' %
                                    # (proto.EVKIT_PROTOCOL_VERSION_MAJOR, proto.EVKIT_PROTOCOL_VERSION_MINOR,
                                     # major_version, minor_version))
            logger.critical('Wrong protocol version received from Firmware. Expected %d.%d, received %d.%d' %
                            (proto.EVKIT_PROTOCOL_VERSION_MAJOR, proto.EVKIT_PROTOCOL_VERSION_MINOR,
                             major_version, minor_version))

    # fixme: combine send_message and receive_message in one with DelayedKeyboardInterrupt():
    def receive_message(self, waif_for_message = None):
        with DelayedKeyboardInterrupt():
            resp = self._kx_connection.receive_message(waif_for_message)
        return resp

    def send_message(self, message):
         with DelayedKeyboardInterrupt():
             self._kx_connection.send_message(message)
    
    def _format_resp(self, data):
        arr=array.array('B')
        if isinstance(data, list):
            arr.fromlist(data)

        elif isinstance(data, int):
            arr.fromlist([data])
            
        elif isinstance(data, str):
            arr.fromstring(data)
        else:
            assert 0,'Unsupported data type %s' % type(data)
            
        return arr
    
    def enable_interrupt(self, pin, payload_definition):
        self.send_message(proto.interrupt_enable_req(pin, payload_definition))
        reponse_data = self.receive_message(proto.EVKIT_MSG_ENABLE_INT_RESP)
        return self._kx_connection.get_stream_id(reponse_data)
        
    def disable_interrupt(self, pin):
        self.send_message(proto.interrupt_disable_req(pin))
        reponse_data = self.receive_message(proto.EVKIT_MSG_DISABLE_INT_RESP)

    def wait_indication(self):
        # TODO consider sending list of accepted messages
        try:
            reponse_data = self.receive_message()
        except proto.ProtocolTimeoutException:
            # timeout is acceptable when waiting indcation message
            return None
        
        msg_id, payload = proto.unpack_response_data(reponse_data)
        return self._format_resp(payload)

    def read_register(self, sensor, register, length=1):
        sad = self._sensortable[sensor]
        self.send_message(proto.read_req(sad, register, length))
        resp = self.receive_message(proto.EVKIT_MSG_READ_RESP)
        try:
            resp = proto.unpack_response_data(resp)
        except proto.ProtocolBus1Exception:
            raise BusException('No response from bus 1')
        
        return self._format_resp(resp[1])    
    
    def write_register(self, sensor, register, value):
        sad = self._sensortable[sensor]
        self.send_message(proto.write_req(sad, register, value))
        self.receive_message(proto.EVKIT_MSG_WRITE_RESP)

    def gpio_read(self, gpio):
        "Reads physical GPIO pin"
        self.send_message(proto.gpio_state_req(gpio))
        resp = self.receive_message(proto.EVKIT_MSG_GPIO_STATE_RESP)
        return proto.unpack_response_data(resp)[1]
        
    def poll_gpio(self, index):
        "Polls logical GPIO pin"
        #print 'gpio poll',index
        assert index in self.bus_gpio_list
        return self.gpio_read(self._gpio_pin_index[index-1])

class bus_socket(kx_protocol_bus):
    def __init__(self, index = 1):
        self.socket_module_index = [proto.kx_socket_b2s, proto.kx_socket_adb]
        self.index = index

        kx_protocol_bus.__init__(self)        
        self._configure_interrupts()

    def _configure_interrupts(self):
        self.bus_gpio_list = []
        self._gpio_pin_index = []

        for t in range(1,4):
            if not evkit_config.has_option('protocol_gpio','pin%d_index' % t):
                break
            self._has_gpio = True
            self.bus_gpio_list.append(t)
            self._gpio_pin_index.append(evkit_config.getint('protocol_gpio','pin%d_index' % t))

    def open(self):
        kx_protocol_bus.open(self)
        self._kx_port = self.socket_module_index[self.index](timeout = 3)
        self._kx_connection = proto.ProtocolEngine(self._kx_port)

        # run version request
        # FIXME improve
        try:
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)
        except proto.ProtocolException:
            raise proto.ProtocolException('No response from socket')
        try:
            message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)
        except Exception,e:
            # retry if error
            logger.debug('Version REQ failed. Flushing data and retry.')
            sleep(0.1)
            self._kx_port.flush()
            sleep(0.1)
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)
            message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)

        self.verify_protocol_version(major_version, minor_version)

class bus_serial_com(kx_protocol_bus):
    def __init__(self, index = None ):
        # FIXME consider removing index
        kx_protocol_bus.__init__(self)        
        self.config_section = evkit_config.get('__com__','config')
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

        drdy_op = evkit_config.get('generic', 'drdy_operation') # Warn user if using interrupts and interrupt pin list is empty
        if self.bus_gpio_list == [] and drdy_op.startswith('ADAPTER_GPIO') :
            logger.critical('No interrupt pins configured in setting.cfg!')
    
    def get_com_port(self):
        if self.config_section == 'serial_com_kx_iot':
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'USB Serial Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            
        elif self.config_section.startswith('serial_com_nrf51dk'):
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'mbed Serial Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            if result == None:
                result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'JLink CDC UART Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")

        else:
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'Arduino Uno' AND NOT PNPDeviceID LIKE 'ROOT\\%'")

        if result == None:
            raise BusException('Automatic search found no devices')
        else:
            logger.info('Automatic port choice: %s', result)
            return result
        
    def check_com_port(self, wql):
        try:
            import wmi
        except ImportError:
            print "\nPlease run \'pip install wmi\'\nand \'pip install pypiwin32\'\n"
            print "Alternatively define port manyally to settings.cfg\n"
            print "Example for windows OS : com_port = COM10\n"
            print "Example for Linux OS: com_port = /dev/ttyUSB0\n"
            raise

        c = wmi.WMI()
        result = None

        for foundPort in c.query(wql):
            result = foundPort.Name.partition('(')[2].partition(')')[0]
        return result

    def open(self):
        kx_protocol_bus.open(self)
        config_section = evkit_config.get('__com__','config')

        if evkit_config.get(config_section, 'com_port').lower() == 'auto' and os.name == 'posix':
            logger.critical('Automatic port search does not work on linux!')
        if evkit_config.get(config_section, 'com_port').lower() == "auto":
            comport = self.get_com_port()            
        else:    
            comport = evkit_config.get(config_section, 'com_port')
 
        baudrate = evkit_config.getint(config_section, 'baudrate')
        delay_s = evkit_config.getint(config_section, 'start_delay_s')
        self._kx_port = proto.kx_com_port(comport,baudrate, timeout = 1)
        self._kx_connection = proto.ProtocolEngine(self._kx_port)

        if delay_s>0:
            logger.info('Waiting %d seconds', delay_s)
            sleep(delay_s)

        # run version request
        # FIXME improve
        try:
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)
        except proto.ProtocolException:
            raise proto.ProtocolException('No response from %s. Please check COM port number and baudrate and that device is powered on.' % comport)
        try:
            message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)
        except Exception,e:
            # retry if error
            logger.debug('Version REQ failed. Flushing data and retry.')
            sleep(0.1)
            self._kx_port.flush()
            sleep(0.1)
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)
            message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)

        self.verify_protocol_version(major_version, minor_version)
        
