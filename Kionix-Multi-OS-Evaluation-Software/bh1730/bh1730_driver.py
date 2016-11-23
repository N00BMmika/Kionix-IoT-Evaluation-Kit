# The MIT License (MIT)
#
# Copyright 2016 Kionix Inc.
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
        pass
        
    def ic_test(self):
        pass
        
    def set_default_on(self):
        self.set_power_on()
        self.write_register(r.BH1730_TIMING,0xda)

    def read_data(self):
        data = self.read_register(r.BH1730_DATA0LOW,4)
        return struct.unpack('hh',data)

    def read_drdy(self):
        return self.read_register(r.BH1730_CONTROL)[0] & b.BH1730_CONTROL_ADC_VALID != 0

        
    def set_power_on(self): 
        self.write_register(r.BH1730_CONTROL, b.BH1730_CONTROL_POWER |  b.BH1730_CONTROL_ADC_EN)
        
    def set_power_off(self):
        self.set_bit(r.BH1730_CONTROL, 0)
        
    def set_odr(self, valuex):
        self.write_register(r.BH1730_TIMING, valuex)

        
        
