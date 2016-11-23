# 
# Copyright 2016 Kionix Inc.
#
from bus_base import _i2c_bus, BusException
from util_lib import logger, evkit_config
import array

smbus_found = False
gpio_found = False

try:
    import smbus
    smbus_found = True
except ImportError:
    pass

try:
    import gpio
    gpio_found = True
    gpio.log.setLevel(gpio.logging.ERROR)

except ImportError:
    logger.warning('Python GPIO module not installed. '+
                   'Only register polling can be used. '+
                   'Please consider: "pip install GPIO"')
    pass
    

class bus_linux_i2c(_i2c_bus):
    # TODO demonstarte how to put sensor to hs mode
    def __init__(self, aadvark_index = None ):
        _i2c_bus.__init__(self)
        self._handle = None
        if not smbus_found:
            raise BusException('Please install smbus python module: sudo apt-get install python-smbus')
        if gpio_found:
            self._has_gpio = True
            self.bus_gpio_list = [1,2]
            self._gpio_pin_index=[
                evkit_config.getint('linux_gpio','pin1_index'),
                evkit_config.getint('linux_gpio','pin2_index')
                ]
            # TODO synch logic with bus_serial
            gpio.setup(self._gpio_pin_index[0],gpio.IN)
            gpio.setup(self._gpio_pin_index[1],gpio.IN)

            if self.check_are_we_on_raspi(): #disable SPI if on raspi
                logger.debug ('This is Raspberry Pi: Disabling SPI bus so we can use I2C')
                gpio.setup(10,gpio.IN) #MOSI
                gpio.setup(9,gpio.IN)  #MISO
                gpio.setup(11,gpio.IN) #SCLK
            else:
                logger.debug('This is not Raspberry Pi.')

    def check_are_we_on_raspi(self):
        with open ('/proc/cpuinfo') as filetti:
            for line in filetti.readlines():
                if line.find('CPU part') is not -1:
                    if (line.find('0xc07') is not -1 or #raspi2
                        line.find('0xd03') is not -1 or #raspi3
                        line.find('0xb76') is not -1):  #raspi1
                        return 1 #Yes raspi found
            return 0 #this is no raspi

    def configure(self, cfg):
        pass

    def get_configuration_template(self):
        return {}
    
    def open(self, index = 1):
        _i2c_bus.open(self)
        self._handle = smbus.SMBus(index)

    def read_register(self, sensor, register, length=1):
        arr = array.array('B')
        sad = self._sensortable[sensor]
        resp = ''
        for t in range(length):
            for i in range(5):
                try:
                    data = self._handle.read_byte_data(sad, register)

                    register+=1
                    resp+=chr(data)
                    if len(resp)==length:
                        arr.fromstring(resp)
                        return arr


                    break
                except(IOError):
                    #logger.debug('Slave not responding at address %x' % sad)
                    continue

        raise BusException('No response from I2C slave at address 0x%x for sensor %s' % (sad,sensor))
        
        
    def write_register(self, sensor, register, data):
        sad = self._sensortable[sensor]
        self._handle.write_byte_data(sad, register, data)

    def poll_gpio(self, index):
        assert index in self.bus_gpio_list
        return gpio.read(self._gpio_pin_index[index-1])
