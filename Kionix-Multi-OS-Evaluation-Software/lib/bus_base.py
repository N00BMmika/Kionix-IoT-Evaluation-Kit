# 
# Copyright 2016 Kionix Inc.
#
"""Bus definitions for kionix command line evaluation kit"""
from util_lib import evkit_config, logger

class BusException(Exception): pass

""" HAL for digital bus"""
class _bus_base(object):
    def __init__(self):
        self._has_gpio = False
        self._is_open = False
        self._sensortable = {} # dictionary listing sensors in this bus
        self.bus_gpio_list = []

##    def set_bus_speed(self):
##        raise NotImplementedError
##
##    def get_bus_speed(self):
##        raise NotImplementedError

    def has_gpio(self):
        return self._has_gpio

    def enumerate_gpio(self):
        return self.bus_gpio_list

    def _flush_input(self): pass
    
##    def set_gpio_as_input(self, index):
##        raise NotImplementedError
##
##    def set_gpio_as_output(self, index):
##        raise NotImplementedError
        
    def set_gpio(self, index, value):
        raise NotImplementedError

    def poll_gpio(self, index, value):
        raise NotImplementedError

    def get_configuration_template(self):
        raise NotImplementedError
        
    def register_gpio_callback(self, gpio_index, callback = None):
        raise NotImplementedError

##    def unregister_gpio_callback(self, gpio_index):
##        raise NotImplementedError
    
    def write_register(self, register, value):
        raise NotImplementedError

##    def set_registers(register, values):
##        raise NotImplementedError
##
    def read_register(self, register, value, lenght = 1):
        raise NotImplementedError

    def open(self):
        assert (self._is_open == False)
        self._is_open = True

    def close(self):
        assert (self._is_open == True)
        self._is_open = False

##    def get_status_string(self, res):
##        raise NotImplementedError

    def configure(self):
        raise NotImplementedError

class _i2c_bus(_bus_base):
    def __init__(self):
        _bus_base.__init__(self)

    def get_address_for_sensor(self,sensor):
        return self._sensortable[sensor]
        
    def probe_sensor(self, sensor):
        """
        Tries to find sensor with its slave address (SAD) number in this bus. If sensor is found, assign
        this bus to sensor driver, if sensor is not found, clear assigned bus from sensor driver.
        :return: True,  Sensor is found (and this bus assigned to it)
                 False, Sensor is not found (and None-bus is assigned to it)
        """
        if not (sensor.I2C_SUPPORT):
            self.close() # close bus
            raise BusException('Sensor driver %s does not support I2C bus.' % sensor.name)
            return False
        
        #fixme: only first matching sensor is supported. Add support for another SAD in same bus.
        #       (check _sensortable first, and skip existing SADs before assigning and probing)
        found = False
        logger.info('Probe with %s' , sensor.name)
        for sad in sensor.I2C_SAD_LIST:
            self._sensortable[sensor]=sad
            sensor.assign_bus(self)
            try:
                resp = sensor.probe()
                if resp:
                    found = True
                    logger.info('Sensor found from slave address 0x%02x' , sad) 
                    break
                else:
                    logger.debug('Probe failed at slave address 0x%02x' , sad) 
            except BusException:
                logger.debug('No response got from slave address 0x%02x' , sad)

        if not found:
            self._sensortable[sensor]=None
            sensor.assign_bus(None)
            logger.debug('Driver "%s" did not found sensor from I2C bus.' % sensor.name)
        #else keep assigned bus
        
        return found

class _spi_bus(_bus_base):
    def __init__(self):
        _bus_base.__init__(self)
        
    def probe_sensor(self, sensor):
        """
        If sensor is found, assign this bus to sensor driver, if sensor is not found, clear assigned
        bus from sensor driver.
        :return: True,  Sensor is found (and this bus assigned to it)
                 False, Sensor is not found (and None-bus is assigned to it)
        """
        if not (sensor.SPI_SUPPORT):
            self.close() # close bus
            raise BusException('Sensor driver %s does not support SPI bus.' % sensor.name)
            return False

        found = False
        # todo loop through chip select gpio pins
        # when probing sensor, store gpio configuration to
        # self._sensortable

        sensor.assign_bus(self)
        try:
            resp = sensor.probe()
            if resp:
                found = True
            else:
                found = False
        except BusException:
            found = False
            logger.info('BusException; No SPI sensor found.')

        if not found:
            sensor.assign_bus(None)
            logger.debug('Driver "%s" did not found sensor from SPI bus.' % sensor.name)
        #else keep assigned bus
        
        return found
