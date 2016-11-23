# 
# Copyright 2016 Kionix Inc.
#
from util_lib import *
#FIXME need to check that bus supports same number of interrputs that sensor has

import traceback

class SensorException(Exception): pass

class sensor_base(object):
    "Sensor interface definition"
    I2C_SAD_LIST = [] # list of possible i2c slave addresses of sensor
    SPI_SUPPORT = False
    I2C_SUPPORT = False
    INT_PINS = []
    INT1_ACTIVE_HIGH = True     #Default value is overwritten in init with config value (if found).
    INT2_ACTIVE_HIGH = True
    USE_ADAPTER_INT_PINS = False

    def __init__(self):
        self._dump_range = None
        self._registers = None
        self._bus = None
        self.name = self.__class__.__name__
        self.poll_delay_s = evkit_config.getint('generic', 'drdy_poll_interval') / 1000.
        self.WHOAMI = None
        self.drdy_LUT={
            'INTERVAL_READ':self._poll_delay,
            'DRDY_REG_POLL':self._poll_drdy_register,
            'ADAPTER_GPIO1_INT':self._poll_gpio_line1,
            'ADAPTER_GPIO2_INT':self._poll_gpio_line2
            }
        self.truefalse_LUT={
            'TRUE':True,
            'FALSE':False
            }

        logger.debug('Using %s for data ready.' % evkit_config.get('generic', 'drdy_operation'))

        # dynamic definition for function used for data delaying sensor data reading
        self.drdy_function = self.drdy_LUT[evkit_config.get('generic', 'drdy_operation')]
        try:
            self.INT1_ACTIVE_HIGH = self.truefalse_LUT[(evkit_config.get('generic', 'int1_active_high')).upper()]
        except ConfigParser.NoOptionError:
            pass    #keyword not found in settings, keep default value
        try:
            self.INT2_ACTIVE_HIGH = self.truefalse_LUT[(evkit_config.get('generic', 'int2_active_high')).upper()]
        except ConfigParser.NoOptionError:
            pass    #keyword not found in settings, keep default value
        try:
            self.USE_ADAPTER_INT_PINS = self.truefalse_LUT[(evkit_config.get('generic', 'use_adapter_int_pins')).upper()]
        except ConfigParser.NoOptionError:
            pass    #keyword not found in settings, keep default value

#
# Sensor driver interface
#
    def drdy_function(self):
        "This will be overwritten in __init__()"
        pass
        
    def assign_bus(self, bus):
        """
        Setting up connection bus to sensor object.
        """
        self._bus = bus
        if ( self._bus != None ):
            if( self._bus.has_gpio() == False ):
                self.USE_ADAPTER_INT_PINS = False       #Regardless of settigns, don't try to use adapter gpio as int if adapter doesn't have gpio.

#Mandatory functions for each driver:
    def probe(self):
        """
        Read sensor ID register and make sure value is expected one.
        :return: 0, Sensor ID not found on bus
                 1, Sensor ID is found on bus
        """
        raise NotImplementedError

    def por(self):  #a.k.a. soft_reset()
        """
        Initiate software reset (reset without cutting voltage supply or ground wires).
        """
        raise NotImplementedError

    def ic_test(self):
        """
        Test of register writing. Ic should be responsive to bus (powered on) before calling this function.
        Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
        This function can contain one or many tests which confirm that ic chip is working.
        """
        raise NotImplementedError

    def set_default_on(self):
        """
        Power on sensor and configure defaults. This function is used to start real measurements with minimal effort.
        """
        raise NotImplementedError

    def read_data(self):
        """
        Read measurement data from sensor registers. Return data in tuple even when only one value is returned.
        If multiple data sources are available, additional parameter can be given. Additional parameter must
        have default value set to be used if no parameter is given by caller.
        :return: (data) or (data1, data2, ...)
        """
        raise NotImplementedError

#Common optional functions
    def read_drdy(self):#read_drdy_reg
        """
        Used by framework for poll loop. Poll data ready register via i2c, return register status True/False
        If multiple drdy registers are available, additional parameter can be given. Additional parameter must
        have default value set to be used if no parameter is given by caller. Additional parameter must correlate
        with read_data additional parameter.
        :return: True/False
        """
        raise NotImplementedError

##Function names for enabled/disable -type functions:
# is_*_enabled() , for example      is_drdy_pin_enabled()
# enable_*()     , for example  enable_drdy_pin()
# disable_*()    , for example disable_drdy_pin()
##


#
#   Common methods implemented in base class
#
    #Write value to sensor register via bus.
    def write_register(self, register, value):
        if 0:
            #print '<reg_write>%s,0x%02X,0x%02X</reg_write>' % (self.__module__.split('_driver')[0].upper(), register, value)
            stack_list = traceback.extract_stack()[-3]
            #print stack_list
            s2 = stack_list[-1]
            s1 = stack_list[-2]
            stack = s1+'/'+s2
            print 'b.write_register(%s,0x%02X,0x%02X)\t# %s' % (self.__module__.split('_driver')[0].upper(), register, value, stack)
            #print stack
        self._bus.write_register(self, register, value)


    #Read value from sensor register via bus.
    def read_register(self, register, length=1):
        return self._bus.read_register(self, register, length)

    #Set input bit 1 bit(s) as 1 in target register by read/change/write -cycle. Keep zeroes in input bit as they are in register.
    def set_bit(self,register, bit):
        value = self.read_register(register)[0]
        value = value | bit
        self.write_register(register, value)

    #Set input bit 1 bit(s) to 0 in target register by read/change/write -cycle. Keep zeroes in input bit as they are in register.
    def reset_bit(self, register, bit):
        value = self.read_register(register)[0]
        value = value & ~bit
        self.write_register(register, value)

    #Change masked bits in target register by read/change/write -cycle. Keep other bits.
    def set_bit_pattern(self, register, bit_pattern, mask):
        value = self.read_register(register)[0] & ~ mask
        value |= bit_pattern
        self.write_register(register, value)

    def register_dump(self):
        """
        Printout values from all registers in _dump_range.
        """
        self.register_dump_range()

    def register_dump_range(self, startreg=0, endreg=0):
        """
        Printout values from registers in _dump_range (_dump_range is set in driver). Incomplete
        range can be given with parameters.
        :param startreg: first register address to printout
        :param endreg:    last register address to printout
        """
        if (endreg==0):
            startreg, endreg = self._dump_range
        reg_list = range( startreg, (endreg + 1) )
        self.register_dump_listed(reg_list)
        return

    def register_dump_listed(self, reglist):
        """
        Printout values from registers in reglist.
        :param reglist: list of registers
        """
        k=self._registers.keys()
        v=self._registers.values()
        for reg in reglist:
            try:
                i = v.index(reg)
            except ValueError:
                continue
            name = k[i]
            name=name.ljust(20)
            d = self.read_register(reg)[0]
            print '0x%02x %s\t0x%02x\t%s' % (reg ,name, d, '0b{0:08b}'.format(d))

    def address(self):
        "returns address where sensor was found. For example i2c address"
        return self._bus.get_address_for_sensor(self)

#
#
#
    def _poll_delay(self):
        time.sleep(self.poll_delay_s )
        return 0

    def _poll_drdy_register(self, timeout = 5000):
        """Wait for data ready register value change.

            Returns
                0  if successfully seend gpio line change
                -1 if no gpio line change not seen
        """
        count=0
        while not self.read_drdy():
            count+=1
            if timeout and count > timeout:
                logger.error('DRDY not detected. Please check sensor configuration.')
                return -1
            
        if count == 0:
            logger.error('Data overflow. ODR too high for host adapter.')
            return -1
        return 0

    def _poll_gpio_line1(self, timeout = 5000):
        return self.bus_poll_gpio(1, active_high=self.INT1_ACTIVE_HIGH, timeout=timeout)

    def _poll_gpio_line2(self, timeout = 5000):
        return self.bus_poll_gpio(2, active_high=self.INT2_ACTIVE_HIGH, timeout=timeout)

    def bus_poll_gpio(self, gpio_number, active_high=True, timeout = 5000):
        """Wait for data ready gpio line change.

            Returns
                0  if successfully seend gpio line change
                -1 if no gpio line change not seen
        """
        assert gpio_number in self._bus.bus_gpio_list,'Interrupt %d not supported in selected bus.' % gpio_number

        count=0
        if (active_high==True):
            active = 1
        else:
            active = 0

        while ( self._bus.poll_gpio(gpio_number) != active):
            count+=1
            if timeout and count > timeout:
                assert 0,'No interrupts received. Please check interrupt line connections and sensor configuration.'
        if count == 0:
            logger.warning('Data overflow. ODR too high for host adapter or GPIO lines not connected')
            return -1
        return 0

    def is_use_adapter_int_pins_enabled(self):
        """
        :return True:  Program should use adapter gpio for interrupt polling.
        :return False: Program should use sensor registers for interrupt polling.
        """
        return self.USE_ADAPTER_INT_PINS

