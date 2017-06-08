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
from lib.sensor_base import sensor_base

import kxcnl_registers as sensor
r = sensor.registers()
b = sensor.bits()
m = sensor.masks()

class kxcnl_driver(sensor_base):
    _WAI = 0x0B

    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x1D, 0x1E]
        self.SPI_SUPPORT = False
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        self._registers = dict(r.__dict__)
        self._dump_range = (r.KXCNL_CNTL1, r.KXCNL_OUTS2)

    def probe(self):
        resp = self.read_register(r.KXCNL_WIA)
        if resp[0] == self._WAI:
            self.WHOAMI = resp[0]
            logger.info('KXCNL found')            
            return 1
        logger.debug("wrong WHOAMI received for KXCNL: 0x%02x" % resp[0])         
        return 0
        
    def por(self):
        self.write_register(r.KXCNL_CNTL4, b.KXCNL_CNTL4_STRT)
        delay_seconds(1)
        logger.debug("POR done")        

    def read_data(self, channel=CH_ACC):
        assert channel == CH_ACC, 'Only CH_ACC channel supported' ## 
        data = self.read_register(r.KXCNL_OUTX_L,6)
        return struct.unpack('hhh',data)

    def read_drdy(self, intpin=1, channel=CH_ACC):
        ## TODO; maybe suitable state program is capable for latched data ready
        # data ready does not latch off when reading data
        drdy = self.read_register(r.KXCNL_STAT)[0] & b.KXCNL_STAT_DRDY != 0
        logger.warning('DRDY register polling unreliable with Aardvark')
        return drdy

    def set_default_on(self):
        """
        2g, 25hz, dataready to INT1 latched active low
        """
        ## set odr        
        self.set_odr(b.KXCNL_CNTL1_ODR_25)

        ## set range
        self.set_range(b.KXCNL_CNTL1_SC_2G)

        ## interrupts
        self.enable_drdy(intpin=1)         
        self.set_bit(r.KXCNL_CNTL1, b.KXCNL_CNTL1_IEN)      # physical interrupts enabled
        self.reset_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_IEL)    # latched interrupt
        self.reset_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_IEA)    # active low
                    
        self.set_power_on()
        #self.release_interrupts()                           # clear interrupts
        
    def set_odr(self, odr, channel=CH_ACC):
        self.set_bit_pattern(r.KXCNL_CNTL1, odr, m.KXCNL_CNTL1_ODR_MASK)

    def set_power_on(self, channel=CH_ACC):
        self.set_bit(r.KXCNL_CNTL1, b.KXCNL_CNTL1_PC)

    def set_power_off(self, channel=CH_ACC):
        self.reset_bit(r.KXCNL_CNTL1, b.KXCNL_CNTL1_PC)

    def set_range(self, range, temp=0, channel=CH_ACC):
        self.set_bit_pattern(r.KXCNL_CNTL1, range, m.KXCNL_CNTL1_SC_MASK)
       
    def enable_drdy(self, intpin=1, channel=CH_ACC):
        ## TODO; maybe suitable state program is capable for latched data ready
        assert intpin == 1,'KXCNL supports only DRDY to pin1'
        self.set_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_DR_EN)    # Data Ready signal is connected to INT1 and overrides any other interrupt settings.
        self.set_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_INT1_EN)  # INT1/DRDY signal enabled and signal is fully functional.
        
    def disable_drdy(self, intpin=1, channel=CH_ACC):
        ## TODO; maybe suitable state program is capable for latched data ready        
        assert intpin == 1,'KXCNL supports only DRDY to pin1'
        self.reset_bit(r.KXCNL_CNTL1, b.KXCNL_CNTL1_IEN) # physical interrupts enabled. Is this needed?
        self.reset_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_INT1_EN) # INT1/DRDY signal enabled and signal is fully functional.
        
    def release_interrupts(self, intpin=1):
        # TODO consider to check IEN bit also before handling state machine interrupts
        cntl2 = self.read_register(r.KXCNL_CNTL2)[0] # state machine 1 settings
        cntl3 = self.read_register(r.KXCNL_CNTL3)[0] # state machine 2 settings

        if intpin == 1:
            if ((cntl2 & b.KXCNL_CNTL2_SM1_EN) and (cntl2 & b.KXCNL_CNTL2_SM1_PIN ==0)): # sm1 active and routed to pin 1
                self.read_register(r.KXCNL_OUTS1)
            if ((cntl3 & b.KXCNL_CNTL3_SM2_EN) and (cntl3 & b.KXCNL_CNTL3_SM2_PIN ==0)): # sm2 active and routed to pin 1
                self.read_register(r.KXCNL_OUTS2)
        if intpin == 2:
            if ((cntl2 & b.KXCNL_CNTL2_SM1_EN) and (cntl2 & b.KXCNL_CNTL2_SM1_PIN ==2)): # sm1 active and routed to pin 2
                self.read_register(r.KXCNL_OUTS1)
            if ((cntl3 & b.KXCNL_CNTL3_SM2_EN) and (cntl3 & b.KXCNL_CNTL3_SM2_PIN ==2)): # sm2 active and routed to pin 2
                self.read_register(r.KXCNL_OUTS2)



