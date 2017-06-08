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

import bh1790_registers as sensor
r=sensor.registers()
b=sensor.bits()
m=sensor.masks()
e=sensor.enums()

class bh1790_driver(sensor_base):
    _WAI = b.BH1790_PART_ID_WIA_ID
    
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x5B]
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        self._registers = dict(r.__dict__)
        self._dump_range = (r.BH1790_MANUFACTURER_ID, r.BH1790_DATAOUT_LEDON_H)

    def probe(self):
        resp = self.read_register(r.BH1790_PART_ID)
        if resp[0] == self._WAI:
            return 1
        return 0

    def por(self):
        self.write_register(r.BH1790_RESET, b.BH1790_RESET_SWRESET)
        
    def ic_test(self):
        pass
        
    def set_default_on(self):
        self.set_power_on()
        self.set_led_freq_128hz()
        self.set_odr(b.BH1790_MEAS_CONTROL1_RCYCLE_64HZ)
        self.set_led_pulsed(1)
        self.set_led_pulsed(2)
        self.set_led_on_time_216us()
        self.set_led_current(b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA)
        self.start_measurement()

    def read_data(self):
        data = self.read_register(r.BH1790_DATAOUT_LEDOFF_L,4)
        return struct.unpack('HH',data)

    def read_drdy(self):    #no drdy or interrupt register
        return 1
        
    def set_power_on(self): 
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, b.BH1790_MEAS_CONTROL1_RDY_ENABLE, m.BH1790_MEAS_CONTROL1_RDY_MASK)
        
    def set_power_off(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, b.BH1790_MEAS_CONTROL1_RDY_DISABLE, m.BH1790_MEAS_CONTROL1_RDY_MASK)

    def start_measurement(self):
        self.set_bit_pattern(r.BH1790_MEAS_START, b.BH1790_MEAS_START_MEAS_ST_START, m.BH1790_MEAS_START_MEAS_ST_MASK)

    def stop_measurement(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, b.BH1790_MEAS_CONTROL1_RDY_DISABLE, m.BH1790_MEAS_CONTROL1_RDY_MASK)

    def set_led_constant(self, led):
        assert (led) in [1,2]
        if (led == 1):
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED1_EN_CONSTANT, m.BH1790_MEAS_CONTROL2_LED1_EN_MASK)
        elif (led == 2):
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED2_EN_CONSTANT, m.BH1790_MEAS_CONTROL2_LED2_EN_MASK)

    def set_led_pulsed(self, led):
        assert (led) in [1,2]
        if (led == 1):
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED1_EN_PULSED, m.BH1790_MEAS_CONTROL2_LED1_EN_MASK)
        elif (led == 2):
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED2_EN_PULSED, m.BH1790_MEAS_CONTROL2_LED2_EN_MASK)            

        
    def set_led_current(self, led_current):
        assert (led_current) in [   b.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA,  \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA,  \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA,  \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA,  \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA,  \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA, \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA, \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA, \
                                    b.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA]
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, led_current, m.BH1790_MEAS_CONTROL2_LED_CURRENT_MASK)

    def set_led_on_time_216us(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED_ON_TIME_216T_OSC, m.BH1790_MEAS_CONTROL2_LED_ON_TIME_MASK)

    def set_led_on_time_432us(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2, b.BH1790_MEAS_CONTROL2_LED_ON_TIME_432T_OSC, m.BH1790_MEAS_CONTROL2_LED_ON_TIME_MASK)        

    def set_led_freq_64hz(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_64HZ, m.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_MASK)

    def set_led_freq_128hz(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_128HZ, m.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_MASK)
        
    def set_odr(self, odr):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1, odr, m.BH1790_MEAS_CONTROL1_RCYCLE_MASK)

