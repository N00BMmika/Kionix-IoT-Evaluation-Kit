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

import kxtj3_registers as sensor
r = sensor.registers()
b = sensor.bits()
m = sensor.masks()

class kxtj3_driver(sensor_base):
    _WAI = [0x35]   # 
    
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x0E, 0x0F]
        self.SPI_SUPPORT = False
        self.I2C_SUPPORT = True
        self.INT_PINS = [1]

        self._registers = dict(r.__dict__)
        self._dump_range = (r.KXTJ3_WHO_AM_I, r.KXTJ3_WU_TH_L)

    def probe(self):
        resp = self.read_register(r.KXTJ3_WHO_AM_I)
        if resp[0] in self._WAI:
            self.WHOAMI = resp[0]
            logger.info('KXTJ3 found')            
            return 1
        logger.debug("wrong WHOAMI received KXTJ3: 0x%02x" % resp[0])       
        return 0
        
    def ic_test(self):
        """ Verify proper integrated circuit functionality """
        dcst1 = self.read_register(r.KXTJ3_DCST_RESP)[0]
        self.set_bit(r.KXTJ3_CTRL_REG2, b.KXTJ3_CTRL_REG2_DCST)
        dcst2 = self.read_register(r.KXTJ3_DCST_RESP)[0]
        
        if dcst1 == 0x55 and dcst2 == 0xaa:
            return True
        return False
    
    def por(self):
        self.write_register(r.KXTJ3_CTRL_REG2, b.KXTJ3_CTRL_REG2_SRST)        
        delay_seconds(1)
        logger.debug("POR done")
        
    def set_power_on(self, channel=CH_ACC):
        self.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_PC)

    def set_power_off(self, channel=CH_ACC):
        self.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_PC)

    def read_data(self, channel=CH_ACC):            # register format for xyz
        data = self.read_register(r.KXTJ3_OUTX_L, 6)
        return struct.unpack('hhh',data)

    def read_drdy(self, intpin=1, channel=CH_ACC):
        return self.read_register(r.KXTJ3_INT_SOURCE1)[0] & b.KXTJ3_INT_SOURCE1_DRDY != 0

    def set_default_on(self):
        """2g, 25hz, high resolution, dataready for INT1, latched active low"""
        self.set_power_off()

        ## select ODR        
        self.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_25)
        
        ## select g-range and 12bit conversion
        self.set_range( b.KXTJ3_CTRL_REG1_GSEL_2G)
        self.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_EN16G)

        ## resolution / power mode selection
        self.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)# high resolution mode

        ## interrupts settings
        self.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)    # enable interrrupt pin
        self.enable_drdy()                # drdy must be enabled also when register polling
        self.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEL)    # latched interrupt
        self.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEA)    # active low

        self.set_power_on()

        self.release_interrupts()       
        self.read_data()  

    def set_odr(self, osa, temp=0, channel=CH_ACC):
        self.set_bit_pattern(r.KXTJ3_DATA_CTRL_REG, osa, m.KXTJ3_DATA_CTRL_REG_OSA_MASK)

    def set_range(self, gsel, temp=0, channel=CH_ACC):
        assert gsel in [b.KXTJ3_CTRL_REG1_GSEL_2G, \
                        b.KXTJ3_CTRL_REG1_GSEL_4G, \
                        b.KXTJ3_CTRL_REG1_GSEL_8G, \
                        b.KXTJ3_CTRL_REG1_GSEL_16G]
        self.set_bit_pattern(r.KXTJ3_CTRL_REG1, gsel, m.KXTJ3_CTRL_REG1_GSEL_MASK)
    
    def enable_drdy(self, intpin=1, channel=CH_ACC):
        assert intpin in self.INT_PINS
        self.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_DRDYE)

    def disable_drdy(self, intpin=1, channel=CH_ACC):
        assert intpin in self.INT_PINS
        self.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_DRDYE)
        self.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)
        
    def release_interrupts(self, intpin=1):
        assert intpin in self.INT_PINS
        self.read_register(r.KXTJ3_INT_REL)

