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
from lib.sensor_base import sensor_base

import bh1730_registers as sensor
r=sensor.registers()
b=sensor.bits()
m=sensor.masks()
e=sensor.enums()

class bh1730_driver(sensor_base):
    _WAI = b.BH1730_OPART_ID_WIA_ID
    
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x29]
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        self._registers = dict(r.__dict__)
        self._dump_range = (r.BH1730_CONTROL, r.BH1730_DATA1HIGH)

    def probe(self):
        resp = self.read_register(r.BH1730_OPART_ID)
        if resp[0] == self._WAI:
            return 1
        return 0

    def por(self):
        self.write_register(r.BH1730_RESET,0x00)
        
    def ic_test(self):
        pass
        
    def set_default_on(self):
        self.set_power_on()
        self.start_measurement()
        self.write_register(r.BH1730_TIMING,0xda)

    def read_data(self):
        data = self.read_register(r.BH1730_DATA0LOW,4)
        return struct.unpack('hh',data)

    def read_drdy(self):
        return self.read_register(r.BH1730_CONTROL)[0] & b.BH1730_CONTROL_ADC_VALID != 0

        
    def set_power_on(self): 
        #self.write_register(r.BH1730_CONTROL, b.BH1730_CONTROL_POWER |  b.BH1730_CONTROL_ADC_EN)
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_POWER_ENABLE, m.BH1730_CONTROL_POWER_MASK)
        
    def set_power_off(self):
        #self.set_bit(r.BH1730_CONTROL, 0)
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_POWER_DISABLE, m.BH1730_CONTROL_POWER_MASK)

    def start_measurement(self):
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_ADC_EN_ENABLE, m.BH1730_CONTROL_ADC_EN_MASK)

    def stop_measurement(self):
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_ADC_EN_DISABLE, m.BH1730_CONTROL_ADC_EN_MASK)
        
    def set_odr(self, valuex):
        self.write_register(r.BH1730_TIMING, valuex)

    def set_gain(self, valuex):
        self.write_register(r.BH1730_GAIN, valuex)

    def clear_interrupt(self):
        self.write_register(r.BH1730_INT_RESET, 0x00)

    def read_interrupt_thresholds(self):
        """
        :return: (uint16, uin16) raw data from (threshold_high, threshold_low)
        """
        data = self.read_register(r.BH1730_THLLOW, (2*2) )
        threshold_high, threshold_low = struct.unpack('HH',data)
        return threshold_high, threshold_low

    def write_interrupt_thresholds(self, threshold_low, threshold_high):
        if not ((0 <= threshold_high) and (threshold_high < 2**16)):
            logger.debug("threshold_high value out of bounds.")
            raise TypeError
        if not ((0 <= threshold_low) and (threshold_low < 2**16)):
            logger.debug("threshold_low value out of bounds.")
            raise TypeError
        THL = ( threshold_high        & 0xff )
        THH = ( threshold_high >> 8 ) & 0xff
        TLL = ( threshold_low         & 0xff )
        TLH = ( threshold_low  >> 8 ) & 0xff
        self.write_register(r.BH1730_THHLOW, THL)
        self.write_register(r.BH1730_THHHIGH, THH)
        self.write_register(r.BH1730_THLLOW, TLL)
        self.write_register(r.BH1730_THLHIGH, TLH)
        return       
        
    def get_interrupt_persistence(self):
        """
        :return: b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function status
        """
        status = self.read_register(r.BH1730_INTERRUPT) & m.BH1730_INTERRUPT_PERSIST_MASK
        return status

    def set_interrupt_persistence(self, persistence):
        """
        :parameter: b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function
        """
        assert (persistence) in [   b.BH1730_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,  \
                                    b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,  \
                                    b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,       \
                                    b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME]
        self.set_bit_pattern(r.BH1730_INTERRUPT, persistence, m.BH1730_INTERRUPT_PERSIST_MASK)
        return

    def enable_int_pin(self):
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_ADC_INTR_ACTIVE, m.BH1730_CONTROL_ADC_INTR_MASK)
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_ONE_TIME_CONTINOUS, m.BH1730_CONTROL_ONE_TIME_MASK)
        self.set_bit_pattern(r.BH1730_INTERRUPT, b.BH1730_INTERRUPT_INT_EN_VALID, m.BH1730_INTERRUPT_INT_EN_MASK)
        self.set_bit_pattern(r.BH1730_INTERRUPT, b.BH1730_INTERRUPT_INT_STOP_CONTINUOUS, m.BH1730_INTERRUPT_INT_STOP_MASK)
        return

    def disable_int_pin(self):
        self.set_bit_pattern(r.BH1730_CONTROL, b.BH1730_CONTROL_ADC_INTR_INACTIVE, m.BH1730_CONTROL_ADC_INTR_MASK)
        return
    
