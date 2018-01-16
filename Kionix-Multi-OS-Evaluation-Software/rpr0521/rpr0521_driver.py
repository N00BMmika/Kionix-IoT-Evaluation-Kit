# The MIT License (MIT)
#
# Copyright (c) 2016 Rohm Semiconductor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
from imports import *

from lib.sensor_base import sensor_base, SensorException

import rpr0521_registers as sensor
r=sensor.registers()
b=sensor.bits()
m=sensor.masks()
e=sensor.enums()

class rpr0521_driver(sensor_base):
    _WAIREG = r.RPR0521_SYSTEM_CONTROL
    _WAI =  ( b.RPR0521_SYSTEM_CONTROL_PART_ID )

    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x38]
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]       #rpr0521 has only one drdy, but it can be connected to either of aardvark gpio pins.


    # Read component ID and compare it to expected value
    def probe(self):
        resp = self.read_register(self._WAIREG)
        if resp[0] == self._WAI:
            # configurations to register_dump()
            self._registers = dict(r.__dict__)
            self._dump_range = (r.RPR0521_REGISTER_DUMP_START, r.RPR0521_REGISTER_DUMP_END)
            return 1
        return 0

        # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
    def ic_test(self):#
         #ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.RPR0521_MODE_CONTROL)[0]
        self.write_register(r.RPR0521_MODE_CONTROL, (datain1 ^ 0x01) )   #toggle between RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF and RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS
        datain2 = self.read_register(r.RPR0521_MODE_CONTROL)[0]
        self.write_register(r.RPR0521_MODE_CONTROL, datain1)
        if datain2 == (datain1 ^ 0x01):
            return True
        return False

    #setup sensor to be ready for default measurements
    def set_default_on(self):#
        self.set_als_data0_gain(b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1)
        self.set_als_data1_gain(b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1)
        self.set_ps_gain(b.RPR0521_PS_CONTROL_PS_GAIN_X1)
        self.set_measurement_time(b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS)
        self.set_ps_int_sensitivity(b.RPR0521_PS_CONTROL_PERSISTENCE_DRDY)
        self.enable_als_ps_measurement()
        return

    def set_power_on(self):
        self.enable_als_ps_measurement()
        return
    
    def set_power_off(self):
        self.disable_als_ps_measurement()
        self.write_register(r.RPR0521_SYSTEM_CONTROL, b.RPR0521_SYSTEM_CONTROL_INT_PIN_HI_Z)
        return

    def read_data(self):
        data = self.read_data_raw()
        self.clear_interrupt()
        return data

    def por(self):
        self.soft_reset()
        return

    def set_measurement_time(self, valuex):
        assert (valuex) in [b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF,        \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS,       \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS,       \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS,      \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS,      \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS,     \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS,    \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS,    \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS,     \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS,    \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF,      \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS,    \
                            b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS]
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, valuex, m.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_MASK)
        return

    def set_ps_operating_mode(self, valuex):
        assert (valuex) in [b.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT,    \
                            b.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_NORMAL]
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, valuex, m.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_MASK)
        return

    def set_als_data0_gain(self, valuex):
        assert (valuex) in [b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1,     \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2,     \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64,    \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128]
        self.set_bit_pattern(r.RPR0521_ALS_PS_CONTROL, valuex, m.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK)
        return

    def set_als_data1_gain(self, valuex):
        assert (valuex) in [b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1,     \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2,     \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64,    \
                            b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128]
        self.set_bit_pattern(r.RPR0521_ALS_PS_CONTROL, valuex, m.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK)
        return

    def set_ps_gain(self, valuex):
        assert (valuex) in [b.RPR0521_PS_CONTROL_PS_GAIN_X1,    \
                            b.RPR0521_PS_CONTROL_PS_GAIN_X2,    \
                            b.RPR0521_PS_CONTROL_PS_GAIN_X4]
        self.set_bit_pattern(r.RPR0521_PS_CONTROL, valuex, m.RPR0521_PS_CONTROL_PS_GAIN_MASK)
        return

    def get_als_data0_gain(self):
        reg_tmp = self.read_register(r.RPR0521_ALS_PS_CONTROL,1)
        als_gain = reg_tmp | m.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK
        return als_gain

    def get_als_data1_gain(self):
        reg_tmp = self.read_register(r.RPR0521_ALS_PS_CONTROL,1)
        als_gain = reg_tmp | m.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK
        return als_gain

    def get_ps_gain(self):
        reg_tmp = self.read_register(r.RPR0521_PS_CONTROL,1)
        ps_gain = reg_tmp | m.RPR0521_PS_CONTROL_PS_GAIN_MASK
        return ps_gain

    def enable_als_ps_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, (b.RPR0521_MODE_CONTROL_ALS_EN_TRUE | b.RPR0521_MODE_CONTROL_PS_EN_TRUE), (m.RPR0521_MODE_CONTROL_ALS_EN_MASK | m.RPR0521_MODE_CONTROL_PS_EN_MASK))
        return

    def enable_als_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, b.RPR0521_MODE_CONTROL_ALS_EN_TRUE, m.RPR0521_MODE_CONTROL_ALS_EN_MASK)
        return

    def enable_ps_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, b.RPR0521_MODE_CONTROL_PS_EN_TRUE, m.RPR0521_MODE_CONTROL_PS_EN_MASK)
        return

    def disable_als_ps_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, (b.RPR0521_MODE_CONTROL_ALS_EN_FALSE | b.RPR0521_MODE_CONTROL_PS_EN_FALSE), (m.RPR0521_MODE_CONTROL_ALS_EN_MASK|m.RPR0521_MODE_CONTROL_PS_EN_MASK))
        return

    def disable_als_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, b.RPR0521_MODE_CONTROL_ALS_EN_FALSE, m.RPR0521_MODE_CONTROL_ALS_EN_MASK)
        return

    def disable_ps_measurement(self):
        self.set_bit_pattern(r.RPR0521_MODE_CONTROL, b.RPR0521_MODE_CONTROL_PS_EN_FALSE, m.RPR0521_MODE_CONTROL_PS_EN_MASK)
        return

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        For this sensor return True if either of Proxy/ALS INT is True.
        """
        interrupt_reg = (self.read_register( r.RPR0521_INTERRUPT ))[0]
        drdybit = interrupt_reg & (m.RPR0521_INTERRUPT_PS_INT_STATUS_MASK)
        drdy_status = ( drdybit == b.RPR0521_INTERRUPT_PS_INT_STATUS_ACTIVE )
        if (drdy_status == True):
            return drdy_status  #True
        drdybit = interrupt_reg & (m.RPR0521_INTERRUPT_ALS_INT_STATUS_MASK)
        drdy_status = ( drdybit == b.RPR0521_INTERRUPT_ALS_INT_STATUS_ACTIVE )
        return drdy_status  #True/False

    def read_data_raw(self):
        data = self.read_register(r.RPR0521_PS_DATA_LSBS,6)
        dataout = struct.unpack('<HHH',data)     #little endian(LowHigh, LowHigh, LowHigh), 16bitPS, 16bitALS0, 16bitALS1
        return dataout

    def soft_reset(self):
        self.write_register(r.RPR0521_SYSTEM_CONTROL,
                            b.RPR0521_SYSTEM_CONTROL_SW_RESET_START | b.RPR0521_SYSTEM_CONTROL_INT_PIN_HI_Z)
        return

    def enable_interrupt_both(self):
        interrupt_reg_new = (   b.RPR0521_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION |
                                b.RPR0521_INTERRUPT_INT_ASSERT_STABLE |
                                b.RPR0521_INTERRUPT_INT_LATCH_ENABLED |
                                b.RPR0521_INTERRUPT_INT_TRIG_BY_BOTH )
        self.write_register(r.RPR0521_INTERRUPT, interrupt_reg_new)
        return

    def enable_interrupt_ps_only(self):
        interrupt_reg_new = (   b.RPR0521_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION |
                                b.RPR0521_INTERRUPT_INT_ASSERT_STABLE |
                                b.RPR0521_INTERRUPT_INT_LATCH_ENABLED |
                                b.RPR0521_INTERRUPT_INT_TRIG_BY_PS )
        self.write_register(r.RPR0521_INTERRUPT, interrupt_reg_new)
        return

    def enable_drdy_int(self):
        self.set_ps_int_sensitivity(b.RPR0521_PS_CONTROL_PERSISTENCE_DRDY)
        self.enable_interrupt_ps_only()
        return

    def disable_drdy_int(self):
        self.write_register(r.RPR0521_INTERRUPT, b.RPR0521_INTERRUPT_INT_TRIG_INACTIVE)
        return

    def set_ps_int_sensitivity(self, valuex):
        """
        Set sensitivity of interrupt.

        intput valuex:  Interrupt is generated after N consecutive measurements if value is
                        outside of limits. N = 0-15. Using 0 will generate interrupt after
                        each measurement regardless of measurement value (~= DRDY).
        """
        assert (valuex) in [b.RPR0521_PS_CONTROL_PERSISTENCE_DRDY,               \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9,      \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10,     \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11,     \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12,     \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13,     \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14,     \
                            b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15]
        self.set_bit_pattern(r.RPR0521_PS_CONTROL, valuex, m.RPR0521_PS_CONTROL_PERSISTENCE_MASK)
        return

    def clear_interrupt(self):
        #self.write_register(r.RPR0521_SYSTEM_CONTROL, b.RPR0521_SYSTEM_CONTROL_INT_PIN_HI_Z)
        self.read_register( r.RPR0521_INTERRUPT )
        return
