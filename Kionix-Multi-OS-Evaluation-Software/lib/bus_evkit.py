# 
# Copyright 2016 Kionix Inc.
#
""" This module
- implements connectivity to all supported connections. 
-- Kionix protocol based connectivity (kx_protocol_bus)
-- Aardvark host adapter
-- Linux native I2C module

"""
from time import sleep
import array
import os

from bus_base import _i2c_bus, BusException
from util_lib import logger, DelayedKeyboardInterrupt, evkit_config
from proto import kx_socket_b2s, kx_socket_adb, kx_com_port, kx_socket_builtin, ProtocolEngine, ProtocolTimeoutException
import proto
from sys import platform as _platform
     
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
    def receive_message(self, waif_for_message = None, cache_messages = True):
        with DelayedKeyboardInterrupt():
            resp = self._kx_connection.receive_message(waif_for_message, cache_messages)
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
        self.socket_module_index = [kx_socket_b2s, kx_socket_adb, kx_socket_builtin]
        self.socket_config_block = ['protocol_gpio','protocol_gpio','rpi3_socket']
        
        #self._kx_socket_b2s = kx_socket_b2s() # For pyreverse
        #self._kx_socket_adb = kx_socket_adb() # For pyreverse
        self.index = index

        kx_protocol_bus.__init__(self)        
        self._configure_interrupts()

    def _configure_interrupts(self):
        self.bus_gpio_list = []
        self._gpio_pin_index = []

        for t in range(1,4): # TODO : now only 4 int lines supported
            if not evkit_config.has_option(
                self.socket_config_block[self.index],'pin%d_index' % t):
                break

            self._has_gpio = True
            self.bus_gpio_list.append(t)
            
            self._gpio_pin_index.append(evkit_config.getint(
                    self.socket_config_block[self.index],'pin%d_index' % t))

    def open(self):
        kx_protocol_bus.open(self)

        if evkit_config.has_option(self.socket_config_block[self.index],'host'):
            host = evkit_config.get(self.socket_config_block[self.index],'host')
        else:
            host = 'localhost'

        if evkit_config.has_option(self.socket_config_block[self.index],'port'):
            port = evkit_config.getint(self.socket_config_block[self.index],'port')
        else:
            port = 8100

        self._kx_port = self.socket_module_index[self.index](host=host, port=port, timeout = 3)
        self._kx_connection = proto.ProtocolEngine(self._kx_port)

        # run version request
        # FIXME improve
        try:
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP, cache_messages = False)
        except proto.ProtocolException:
            raise proto.ProtocolException('No response from socket')
        try:
            message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)
        except Exception,e:
            # retry if error
            logger.warning('Version REQ failed. Flushing data and retry.')
            sleep(0.1)
            self._kx_port.flush()
            sleep(0.1)
            self.send_message(proto.version_req())
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP, cache_messages = False)
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
        # TODO consider using : from serial.tools import list_ports_windows
        if self.config_section == 'serial_com_kx_iot':
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'USB Serial Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            
        elif self.config_section.startswith('serial_com_nrf51dk'):
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'JLink CDC UART Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            if result == None:
                result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'USB Serial Device' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            if result == None:
                result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'mbed Serial Port' AND NOT PNPDeviceID LIKE 'ROOT\\%'")

        elif self.config_section == "serial_com_cypress":
            for desc in ["Cypress USB UART", "USB Serial Device"]:
                result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = '%s' AND NOT PNPDeviceID LIKE 'ROOT\\%%'" % desc)
                if result is not None:
                    break

        else: #Arduino
            result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'Arduino Uno' AND NOT PNPDeviceID LIKE 'ROOT\\%'")
            if result == None:
                result = self.check_com_port("SELECT * FROM Win32_PnPEntity WHERE Description = 'USB Serial Device' AND NOT PNPDeviceID LIKE 'ROOT\\%'")


        if result == None:
            raise BusException('Automatic search found no devices')
        else:
            logger.info('Automatic port choice: %s', result)
            return result
        
    def check_com_port(self, wql):
        try:
            import wmi
        except ImportError:
            logger.critical("Autofinder found no {} devices".format(self.config_section))
            logger.critical("\nPlease run \'pip install wmi\'\nand \'pip install pypiwin32\'\n")
            logger.critical("Alternatively define port in settings.cfg\n")
            logger.critical("Example for windows OS : com_port = COM10\n")
            exit()

        c = wmi.WMI()
        result = None

        for foundPort in c.query(wql):
            result = foundPort.Name.partition('(')[2].partition(')')[0]
        return result

    ############################################################### LINUX SERIAL DEVICE FINDER
    def get_dev(self):
        """Search from /dev for iot node, arduino or nrf-dk depending which config_section is in use

        Returns path to the device
        """

        import glob

        if self.config_section == 'serial_com_kx_iot': #IoT node
            logger.info("Searching for Kx IoT node...")
            dev = glob.glob("/dev/serial/by-id/*usb-FTDI*")

        elif self.config_section.startswith('serial_com_nrf51dk'): #nrf-dk
            logger.info("Searching for NRF5x-dk...")
            dev = glob.glob("/dev/serial/by-id/*SEGGER*")
            if dev == []:
                dev = glob.glob("/dev/serial/by-id/*usb-MBED*")


        elif self.config_section.startswith('serial_com_arduino'): #Arduino
            logger.info("Searching for Arduino...")
            dev = glob.glob("/dev/serial/by-id/*Arduino*")

        else:
            print("Autofinder does not yet support {}",self.config_section )

        if len(dev) == 0:
            logger.critical("Autofinder found no {} devices".format(self.config_section))
            logger.critical("Please define port in settings.cfg")
            logger.critical("Example for Linux OS: com_port = /dev/ttyUSB0")
            exit()


        logger.info("Found {} devices:\n{}".format(len(dev), '\n'.join(dev)))
        logger.info("Using first device found:\n{}".format(dev[0]))
        return dev[0]

    ############################################################### OS X SERIAL DEVICE FINDER
    def get_dev_darwin(self):
        """Search from /dev for iot node, arduino or nrf-dk depending which config_section is in use

        Returns path to the device
        """

        import glob

        if self.config_section == 'serial_com_kx_iot': #IoT node
            logger.info("Searching for Kx IoT node...")
            dev = glob.glob("/dev/tty.usbserial*")

        elif self.config_section.startswith('serial_com_nrf51dk'): #nrf-dk
            logger.info("Searching for NRF5x-dk...")
            dev = glob.glob("/dev/tty.usbmodem*")

        elif self.config_section.startswith('serial_com_arduino'): #Arduino
            logger.info("Searching for Arduino...")
            dev = glob.glob("/dev/tty.usbmodem*")

        else:
            print("Autofinder does not yet support {}",self.config_section )

        if len(dev) == 0:
            logger.critical("Autofinder found no {} devices".format(self.config_section))
            logger.critical("Please define port manually in settings.cfg")
            logger.critical("Example: com_port = /dev/tty.usbserial-DM00336G")
            exit()

        logger.info("Found {} devices:\n{}".format(len(dev), '\n'.join(dev)))
        logger.info("Using first device found:\n{}".format(dev[0]))
        return dev[0]

    def _reset_protocol_engine(self):
        # TODO move to base class and update all child classes
        self._kx_connection = ProtocolEngine(self._kx_port)

    def open(self):
        kx_protocol_bus.open(self)
        
        config_section = evkit_config.get('__com__','config')

        if evkit_config.get(config_section, 'com_port').lower() == 'auto':
            if os.name == 'posix': #Linux etc...
                if _platform == "darwin": # Apple
                    comport = self.get_dev_darwin()
                else: # Linux
                    comport = self.get_dev()
            else:
                comport = self.get_com_port() # windows OS
        else:
            comport = evkit_config.get(config_section, 'com_port')
 
        baudrate = evkit_config.getint(config_section, 'baudrate')
        delay_s = evkit_config.getint(config_section, 'start_delay_s')
        self._kx_port = kx_com_port(comport,baudrate, timeout = 2)
        self._reset_protocol_engine()
        
        if delay_s>0:
            logger.info('Waiting %d seconds', delay_s)
            sleep(delay_s)

        # run version request
        self._kx_port.flush() # Flush com port in case there is already some unwanted data
        self.send_message(proto.version_req())
        # TODO if getting error message instead of EVKIT_MSG_VERSION_RESP, then resend version_req
        
        # TODO congfigure port latency if possible
        # Ref
        # windows user guide 4.1.4. FTDI USB Serial driver and
        # linux  /sys/bus/usb-serial/devices/ttyUSB0/latency_timer
        # https://github.com/pyserial/pyserial/issues/287
        
        try:
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP, cache_messages = False)
        except ProtocolTimeoutException:
            logger.warning('Version REQ failed. Flushing data and retry.')
            self._kx_port.flush() # Flush com port in case there is already some unwanted data
            reponse_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP, cache_messages = False)
        
        message_type, major_version, minor_version = proto.unpack_response_data(reponse_data)
        self.verify_protocol_version(major_version, minor_version)
        
