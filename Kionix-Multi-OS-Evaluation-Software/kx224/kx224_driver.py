# The MIT License (MIT)
#
# Copyright (c) 2016 Kionix Inc.
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

import kx224_registers
r = kx224_registers.registers()
b = kx224_registers.bits()
m = kx224_registers.masks()
e = kx224_registers.enums()

hz = [12.5, 25.0, 50.0, 100.0, \
      200.0, 400.0, 800.0, 1600.0, \
      0.781, 1.563, 3.125, 6.25, \
      3200.0, 6400.0, 12800.0, 25600.0
      ]        # for PC1 start delay (acc) calculation

class kx224_driver(sensor_base):
    _WAIS224 =[b.KX224_WHO_AM_I_WIA_ID,
               b.KX222_WHO_AM_I_WIA_ID]

    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x1E, 0x1F] #
        self.SPI_SUPPORT = True
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

    def probe(self):
        resp = self.read_register(r.KX224_WHO_AM_I)
        if resp[0] in self._WAIS224:
            self.WHOAMI = resp[0]
            if self.WHOAMI in self._WAIS224:
                logger.info('KX222/KX224 found')
                self._registers = dict(r.__dict__)
                self._dump_range = (r.KX224_CNTL1, r.KX224_BUF_CNTL2)
            return 1
        logger.debug("wrong WHOAMI received for KX224: 0x%02x" % resp[0])
        return 0

    def ic_test(self):                      # communication self test
        """verify proper integrated circuit functionality"""
        ctl2 = self.read_register(r.KX224_CNTL2)[0]

        cotr1 = self.read_register(r.KX224_COTR)[0]
        self.write_register(r.KX224_CNTL2,ctl2 | b.KX224_CNTL2_COTC)

        cotr2 = self.read_register(r.KX224_COTR)[0]
        self.write_register(r.KX224_CNTL2,ctl2 & ~b.KX224_CNTL2_COTC)

        if cotr1 == b.KX224_COTR_DCSTR_BEFORE and cotr2 == b.KX224_COTR_DCSTR_AFTER:
            return True
        return False

    def por(self):
        self.write_register(r.KX224_CNTL2, b.KX224_CNTL2_SRST)
        delay_seconds(1)
        logger.debug("POR done")

    def set_power_on(self, channel=CH_ACC):        
        """
        Set operating mode to "operating mode".
        """
        assert channel == CH_ACC, 'only accelerometer available'
        self.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_PC1)
        
        ## When changing PC1 0->1 then 1.5/ODR delay is needed
        odr_t =1 / (hz[self.read_register(r.KX224_ODCNTL,1)[0] & m.KX224_ODCNTL_OSA_MASK]) * 1.5     
        if odr_t < 0.1:
            odr_t = 0.1
        delay_seconds(odr_t) 

    def set_power_off(self, channel=CH_ACC):
        """
        Set operating mode to "stand-by".
        """
        assert channel == CH_ACC, 'only accelerometer available'        
        cntl1 = self.read_register(r.KX224_CNTL1)[0]
        self.write_register(r.KX224_CNTL1, cntl1 & ~b.KX224_CNTL1_PC1)
   
        ## When changing PC1 1->0 then 1.5/ODR delay is needed
        odr_t =1 / hz[self.read_register(r.KX224_ODCNTL,1)[0] & m.KX224_ODCNTL_OSA_MASK] * 1.5
        if odr_t < 0.1:
            odr_t = 0.1   
        delay_seconds(odr_t) 

    def read_data(self, channel=CH_ACC):
        assert channel == CH_ACC, 'only accelerometer available'
        data = self.read_register(r.KX224_XOUT_L,6)
        return struct.unpack('hhh',data)
    
    def read_drdy(self, intpin=1, channel=CH_ACC):
        assert intpin in self.INT_PINS
        assert channel==CH_ACC, 'only accelerometer available'
        return self.read_register(r.KX224_INS2)[0] & b.KX224_INS2_DRDY != 0

    def set_default_on(self):
        """
        2g, 25Hz ODR, high resolution mode, dataready to INT1 latched active low
        """
        self.set_power_off()

        ## select ODR
        self.set_odr(b.KX224_ODCNTL_OSA_25)             # default for basic applications

        ## select g-range
        self.set_range(b.KX224_CNTL1_GSEL_8G)

        ## high resolution mode
        self.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)

        ## interrupt settings
        self.enable_drdy(intpin=1)                      # drdy to INT1
        self.reset_bit(r.KX224_CNTL1, b.KX224_INC1_IEL1)# latched interrupt
        self.reset_bit(r.KX224_INC1, b.KX224_INC1_IEA1) # active low

        ## power on sensor
        self.set_power_on()
        self.release_interrupts()                       # clear all interrupts
        
    def enable_drdy(self, intpin=1, channel=CH_ACC):
        """enables and routes dataready, but not enable physical interrupt"""
        assert channel == CH_ACC, 'only accelerometer available'
        assert intpin in self.INT_PINS
        self.set_bit(r.KX224_CNTL1,  b.KX224_CNTL1_DRDYE)
        if intpin==1:
            self.set_bit(r.KX224_INC4, b.KX224_INC4_DRDYI1)     # data ready to int1
        else:
            self.set_bit(r.KX224_INC6, b.KX224_INC6_DRDYI2)     # data ready to int2
            
    def disable_drdy(self, intpin=1, channel=CH_ACC):
        """disables and routes dataready, but not enable physical interrupt"""
        assert channel == CH_ACC, 'only accelerometer available'
        assert intpin in self.INT_PINS
        self.reset_bit(r.KX224_CNTL1, b.KX224_CNTL1_DRDYE)
        if intpin==1:
            self.reset_bit(r.KX224_INC4, b.KX224_INC4_DRDYI1)     # remove drdy to int1 routing
        else:
            self.reset_bit(r.KX224_INC6, b.KX224_INC6_DRDYI2)     # remove drdy to int2 routing

    def set_odr(self, ODCNTL_OSA, channel=CH_ACC):
        assert channel == CH_ACC, 'only accelerometer available'
        self.set_bit_pattern(r.KX224_ODCNTL, ODCNTL_OSA, m.KX224_ODCNTL_OSA_MASK)

    def set_range(self, range, range2=0, channel=CH_ACC):
        assert channel == CH_ACC, 'only accelerometer available'
        self.set_bit_pattern(r.KX224_CNTL1, \
                               range, \
                               m.KX224_CNTL1_GSEL_MASK)

    def set_interrupt_polarity(self, intpin = 1, polarity = ACTIVE_LOW):
        assert intpin in [1,2]
        assert polarity in [ACTIVE_LOW, ACTIVE_HIGH]

        if intpin == 1:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX224_INC1, b.KX224_INC1_IEA1)   # active low
            else:
                self.set_bit(r.KX224_INC1, b.KX224_INC1_IEA1)     # active high
        else:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX224_INC5, b.KX224_INC5_IEA2)   # active low
            else:
                self.set_bit(r.KX224_INC5, b.KX224_INC5_IEA2)     # active high

    def set_average(self, average, average2=0, channel=CH_ACC):    # set averaging (only for low power)
        assert channel == CH_ACC, 'only accelerometer available'
        assert average in [b.KX224_LP_CNTL_AVC_128_SAMPLE_AVG, \
                           b.KX224_LP_CNTL_AVC_64_SAMPLE_AVG,  \
                           b.KX224_LP_CNTL_AVC_32_SAMPLE_AVG,  \
                           b.KX224_LP_CNTL_AVC_16_SAMPLE_AVG,  \
                           b.KX224_LP_CNTL_AVC_8_SAMPLE_AVG,   \
                           b.KX224_LP_CNTL_AVC_4_SAMPLE_AVG,   \
                           b.KX224_LP_CNTL_AVC_2_SAMPLE_AVG,   \
                           b.KX224_LP_CNTL_AVC_NO_AVG]
        self.set_bit_pattern(r.KX224_LP_CNTL, average, m.KX224_LP_CNTL_AVC_MASK)

    def set_BW(self, lpro=b.KX224_ODCNTL_LPRO,lpro2=0, channel=CH_ACC):
        assert channel == CH_ACC, 'only accelerometer available'         
        assert lpro in [b.KX224_ODCNTL_LPRO, 0]
        if lpro:
            self.set_bit(r.KX224_ODCNTL, b.KX224_ODCNTL_LPRO)   # BW odr /2
        else:
            self.reset_bit(r.KX224_ODCNTL, b.KX224_ODCNTL_LPRO) # BW odr /9 (default)

    def enable_iir(self):
        self.reset_bit(r.KX224_ODCNTL, b.KX224_ODCNTL_IIR_BYPASS)

    def disable_iir(self):
        self.set_bit(r.KX224_ODCNTL, b.KX224_ODCNTL_IIR_BYPASS)

    def release_interrupts(self, intpin=1):
        assert intpin in self.INT_PINS        
        """
        Latched interrupt source information is cleared and physical interrupt latched pin is changed to its inactive state.
        """
        self.read_register(r.KX224_INT_REL) 

    def enable_fifo(self, mode=b.KX224_BUF_CNTL2_BUF_M_STREAM, res=b.KX224_BUF_CNTL2_BRES, axis_mask=0x03): # enable buffer with mode and resolution
        ### syncronized with KXxxx, KXG03
        assert mode < 5, 'not valid buffer mode'
        assert res in [b.KX224_BUF_CNTL2_BRES, 0]       # 8 or 16bit resolution store
        assert axis_mask == 0x03, 'all axis must included to buffer storage with KXx2x'

        if res > 0:
            self.set_bit(r.KX224_BUF_CNTL2, b.KX224_BUF_CNTL2_BRES)
        else:
            self.reset_bit(r.KX224_BUF_CNTL2, b.KX224_BUF_CNTL2_BRES)

        self.set_bit(r.KX224_BUF_CNTL2, b.KX224_BUF_CNTL2_BUFE | mode)

    def disable_fifo(self):                                     # disable buffer
        self.reset_bit(r.KX224_BUF_CNTL2, b.KX224_BUF_CNTL2_BUFE)

    def get_fifo_resolution(self):                              # get resolution 0= 8b, >0 = 16b
        if self.read_register(r.KX224_BUF_CNTL2, 1)[0] & b.KX224_BUF_CNTL2_BRES > 0:
            return 1
        else:
            return 0

    def set_fifo_watermark_level(self, level, axes=3): # hox! set watermark as samples
        assert axes in [3], 'only 3 axes possible to store fifo buffer' 
        if self.get_fifo_resolution() > 0:
            assert level <=0x154,'Watermark level too high.'    # 16b resolution
        else:
            assert level <=0x2A8,'Watermark level too high.'    # 8b resolution
        lsb = level & 0xff
        msb = level >> 8
        self.write_register(r.KX224_BUF_CNTL1, lsb)
        self.set_bit_pattern(r.KX224_BUF_CNTL2,
                             msb << 2,
                             m.KX224_BUF_CNTL2_SMP_TH8_9_MASK)

    def get_fifo_level(self):                                   # hox! get fifo buffer as bytes
        if self.WHOAMI in self._WAIS224:
            bytes_in_buffer = self.read_register(r.KX224_BUF_STATUS_1, 2)
            bytes_in_buffer = bin2uint16(bytes_in_buffer)
            return (bytes_in_buffer & 0x7ff)
        else:
            bytes_in_buffer = self.read_register(r.KX224_BUF_STATUS_1, 1)
            return bin2uint8(bytes_in_buffer)

    def clear_buffer(self):
        self.write_register(r.KX224_BUF_CLEAR, 0xff)

