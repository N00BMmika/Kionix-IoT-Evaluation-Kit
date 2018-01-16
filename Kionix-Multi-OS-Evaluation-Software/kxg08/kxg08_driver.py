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

import kxg08_registers
r = kxg08_registers.registers()
b = kxg08_registers.bits()
m = kxg08_registers.masks()
e = kxg08_registers.enums()

## activity modes
SLEEP, WAKE = range(2)

## wuf and bts_directions
wufbts_direction = {
   b.KXG08_INT1_SRC2_INT1_ZNWU : "FACE_UP",
   b.KXG08_INT1_SRC2_INT1_ZPWU : "FACE_DOWN",
   b.KXG08_INT1_SRC2_INT1_XNWU : "UP",
   b.KXG08_INT1_SRC2_INT1_XPWU : "DOWN",
   b.KXG08_INT1_SRC2_INT1_YPWU : "RIGHT",
   b.KXG08_INT1_SRC2_INT1_YNWU : "LEFT" }

class kxg08_driver(sensor_base):
    _WAIS   = [b.KXG08_WHO_AM_I_WIA_ID,
               b.KXG08_2080_WHO_AM_I_WIA_ID,
               b.KXG07_1080_WHO_AM_I_WIA_ID,
               b.KXG07_2080_WHO_AM_I_WIA_ID,
               b.KXG07_3001_WHO_AM_I_WIA_ID,
              ]
    
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x4E, 0x4F] 
        self.SPI_SUPPORT = True
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.KXG08_WHO_AM_I, r.KXG08_BUF_STATUS)

    def probe(self):
        """
        Read sensor ID register and make sure value is expected one. Return 1 if ID is correct.
        """
        resp = self.read_register(r.KXG08_WHO_AM_I)
        if resp[0] in self._WAIS:
            self.WHOAMI = resp[0]
            if self.WHOAMI == b.KXG08_WHO_AM_I_WIA_ID:                
                logger.info('kxg08-1080 found')
                self.name = 'kxg08_driver'
            elif self.WHOAMI == b.KXG08_2080_WHO_AM_I_WIA_ID:
                logger.info('kxg08-2080 found')
                self.name = 'kxg08_driver'               
            elif self.WHOAMI == b.KXG07_1080_WHO_AM_I_WIA_ID:                
                logger.info('kxg07-1080 found')
                self.name = 'kxg08_driver'                
            elif self.WHOAMI == b.KXG07_2080_WHO_AM_I_WIA_ID:                
                logger.info('kxg07-2080 found')
                self.name = 'kxg08_driver'                
            elif self.WHOAMI == b.KXG07_3001_WHO_AM_I_WIA_ID:                
                logger.info('kxg07-3001 found')
                self.name = 'kxg08_driver'                
            else:
                logger.info("other valid WHOAMI received 0x%02x" % resp[0])
                self.name = 'kxg08_driver'                
            return 1
        logger.debug("wrong WHOAMI received for KXG08: 0x%02x" % resp[0])
        return 0

    def por(self):
        self.write_register(r.KXG08_CTL_REG_1, b.KXG08_CTL_REG_1_SRST)
        logger.debug("Soft Reset")
        timeout = 200
        while timeout > 0:
            time.sleep(0.005)            
            timeout = timeout - 1            
            if (self.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_POR):
                logger.debug("POR done")
                break                                           # POR done
        if timeout == 0:
            raise SensorException('POR failure')
            
    def set_power_on(self, channel = CH_ACC):                   # set sleep and wake modes ON
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel    
        acc_start_delay = 0.0
        gyro_start_delay = 0.0

        if channel & CH_ACC > 0:
            self.set_bit_pattern(r.KXG08_STDBY, b.KXG08_STDBY_ACC_STDBY_ENABLED, \
                                                m.KXG08_STDBY_ACC_STDBY_MASK)
            acc_odr = self.read_register(r.KXG08_ACCEL_ODR,1)[0] & m.KXG08_ACCEL_ODR_ODRA_MASK
            acc_start_delay = 1 / (2**acc_odr * 0.78125) *1.5
            if acc_start_delay < 0.1:
                acc_start_delay = 0.1
      
        if channel & CH_GYRO > 0:
            self.set_bit_pattern(r.KXG08_STDBY, \
                                 b.KXG08_STDBY_GYRO_STDBY_ENABLED |
                                 b.KXG08_STDBY_GYRO_FSTART_DISABLED, \
                                 m.KXG08_STDBY_GYRO_STDBY_MASK | \
                                 m.KXG08_STDBY_GYRO_FSTART_MASK)
            logger.debug("wait gyro start")
            timeout = 200
            while timeout > 0:     # wait for gyro running
                stat = self.read_register(r.KXG08_STATUS1, 1)[0]
                time.sleep(0.005)
                timeout = timeout - 1
                if stat & b.KXG08_STATUS1_GYRO_RUN:
                    break
            if timeout == 0:
                raise SensorException('start failure')
            gyro_start_delay = 0.2 

        if channel & CH_TEMP > 0:
            self.reset_bit(r.KXG08_STDBY, b.KXG08_STDBY_TEMP_STDBY_DISABLED)
            
        if gyro_start_delay > acc_start_delay:
            time.sleep(gyro_start_delay)
        else:
            time.sleep(acc_start_delay)

    def set_power_off(self, channel = CH_ACC | CH_GYRO | CH_TEMP):  # set sleep and wake modes OFF
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel
        acc_end_delay = 0.0
        gyro_end_delay = 0.0
        
        if channel & CH_ACC > 0:
            self.set_bit(r.KXG08_STDBY, b.KXG08_STDBY_ACC_STDBY_DISABLED)
            acc_odr = self.read_register(r.KXG08_ACCEL_ODR,1)[0] & m.KXG08_ACCEL_ODR_ODRA_MASK
            acc_end_delay = 1 / (2**acc_odr * 0.78125) *1.5
            if acc_end_delay < 0.2:
                acc_end_delay = 0.2
                
        if channel & CH_GYRO > 0:
            self.reset_bit(r.KXG08_STDBY, b.KXG08_STDBY_GYRO_FSTART_ENABLED)
            gyro_end_delay = 0.2
            
        if channel & CH_TEMP > 0:
            self.set_bit(r.KXG08_STDBY, b.KXG08_STDBY_TEMP_STDBY_DISABLED)
            
        if gyro_end_delay > acc_end_delay:
            time.sleep(gyro_end_delay)
        else:
            time.sleep(acc_end_delay)

    def read_data(self, channel = CH_ACC | CH_GYRO ):
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel
        s_form = ()
        if channel & CH_TEMP > 0:
            data = self.read_register(r.KXG08_TEMP_OUT_L, 2)
            s_form = s_form + struct.unpack('h', data)
        if channel & CH_GYRO > 0:
            data = self.read_register(r.KXG08_GYRO_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        if channel & CH_ACC > 0:
            data = self.read_register(r.KXG08_ACCEL_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        return s_form

    def read_drdy(self, intpin=1, channel = CH_ACC):            # separated interrupt sources
        assert channel in [CH_ACC, CH_GYRO]
        assert intpin in self.INT_PINS
        if intpin == 1:
            ins1 = self.read_register(r.KXG08_INT1_SRC1)[0]
            if channel & CH_ACC > 0:        
                return ins1 & b.KXG08_INT1_SRC1_INT1_DRDY_ACC != 0
            if channel & CH_GYRO > 0:
                return ins1 & b.KXG08_INT1_SRC1_INT1_DRDY_GYRO != 0
        if intpin == 2:
            ins2 = self.read_register(r.KXG08_INT2_SRC1)[0]
            if channel & CH_ACC > 0:
                return ins2 & b.KXG08_INT2_SRC1_INT2_DRDY_ACC != 0
            if channel & CH_GYRO > 0:
                return ins2 & b.KXG08_INT2_SRC1_INT2_DRDY_GYRO != 0          

    def set_default_on(self):
        """
        ACC+GYRO+temp with full resolution:
            acc 2g/25Hz/BW ODR/8,
            gyro 1024dps/25Hz/BW ODR/8
            interrupt 1, active low, latched
        """
        self.set_odr(b.KXG08_ACCEL_ODR_ODRA_25, channel=CH_ACC)             # acc
        self.set_odr(b.KXG08_GYRO_ODR_ODRG_25, channel=CH_GYRO)             # gyro
        
        self.set_range(b.KXG08_ACCEL_CTL_ACC_FS_2G, channel=CH_ACC)                 # acc
        self.set_range(b.KXG08_GYRO_CTL_GYRO_FS_1024, channel=CH_GYRO)              # gyro
        
        ## mode, averaging and BW for acc+gyro          
		
        #self.set_average(b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG, CH_ACC)   # acc average
        #self.set_average(b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG, CH_GYRO)   # gyro average (only for 2080 version
        ### full resolution mode
        self.set_average(False, CH_ACC)                                     # acc full power
        self.set_average(False, CH_GYRO)                                    # gyro full power

        self.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_8, channel=CH_ACC)         # acc BW
        self.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_8, channel=CH_GYRO)        # gyro BW        

        ## interrupts
        self.enable_drdy(1, CH_ACC)                                         # acc drdy, physical int1
        #self.enable_drdy(1, CH_GYRO)                                       # gyro drdy, physical int1
        self.set_bit(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEN1)
        self.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)        
        self.set_bit_pattern(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEL2_LATCHED | \
                                                  b.KXG08_INT_PIN_CTL_IEL1_LATCHED, \
                                                  m.KXG08_INT_PIN_CTL_IEL2_MASK | \
                                                  m.KXG08_INT_PIN_CTL_IEL1_MASK)  

        self.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)                       # all sensors ON

    def enable_drdy(self, intpin=1, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        assert intpin in self.INT_PINS
        if channel == CH_ACC:
            #enable data ready function
            self.set_bit(r.KXG08_INT_MASK1,         b.KXG08_INT_MASK1_DRDY_ACC)
            
            # route data ready to pin
            if intpin == 1:
                self.set_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_ACC_P1)
            else:
                self.set_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_ACC_P2)
                
        elif channel == CH_GYRO:
            self.set_bit(r.KXG08_INT_MASK1,         b.KXG08_INT_MASK1_DRDY_GYRO)            
            if intpin == 1:
                self.set_bit(r.KXG08_INT_PIN_SEL1,  b.KXG08_INT_PIN_SEL1_DRDY_GYRO_P1)
            else:
                self.set_bit(r.KXG08_INT_PIN_SEL2,  b.KXG08_INT_PIN_SEL2_DRDY_GYRO_P2) 

    def disable_drdy(self, intpin=1, channel = CH_ACC):         # set separately for acc or gyro
        assert channel in [CH_ACC ,CH_GYRO]
        assert intpin in self.INT_PINS
        if channel == CH_ACC:
            self.reset_bit(r.KXG08_INT_MASK1, b.KXG08_INT_MASK1_DRDY_ACC)          
            if intpin == 1:
                self.reset_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_ACC_P1)
            else:
                self.reset_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_ACC_P2)
        elif channel == CH_GYRO:
            self.reset_bit(r.KXG08_INT_MASK1, b.KXG08_INT_MASK1_DRDY_GYRO)
            if intpin == 1:
                self.reset_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_GYRO_P1)
            else:
                self.reset_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_GYRO_P2)

    def set_odr(self, odr, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        if channel == CH_ACC:
            ## value validation
            assert odr in e.KXG08_ACCEL_ODR_ODRA.values(), \
                'Invalid value for acceleropmeter ODR'               
            self.set_bit_pattern(r.KXG08_ACCEL_ODR, odr, m.KXG08_ACCEL_ODR_ODRA_MASK)
        elif channel == CH_GYRO:
            ## value validation
            assert odr in e.KXG08_GYRO_ODR_ODRG.values(), \
                'Invalid value for gyro ODR'              
            self.set_bit_pattern(r.KXG08_GYRO_ODR, odr, m.KXG08_GYRO_ODR_ODRG_MASK)

    def set_range(self, range, channel = CH_ACC):    # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        
        if channel == CH_ACC:
            ## value validation
            assert range in e.KXG08_ACCEL_CTL_ACC_FS.values(), \
                'Invalid value for accelerometer max range'              
            self.set_bit_pattern(r.KXG08_ACCEL_CTL, range, m.KXG08_ACCEL_CTL_ACC_FS_MASK)  
        elif channel == CH_GYRO:
            ## value validation
            assert range in e.KXG08_GYRO_CTL_GYRO_FS.values(), \
                'Invalid value for gyro max range'           
            self.set_bit_pattern(r.KXG08_GYRO_CTL, range, m.KXG08_GYRO_CTL_GYRO_FS_MASK)

    ## sets low power mode AND averaging factor
    def set_average(self, lp_mode, channel = CH_ACC):        # oversampling setting for low power mode
        assert channel in [CH_ACC, CH_GYRO]        

        if channel == CH_ACC:        
            ## value validation
            assert lp_mode in e.KXG08_ACCEL_ODR_NAVGA.values() or lp_mode == False, \
                'Invalid value for accelerometer low power mode. Valid values are: False or %s' % \
                e.KXG08_ACCEL_ODR_NAVGA.keys()
            if lp_mode != False:
                self.set_bit_pattern(r.KXG08_ACCEL_ODR, lp_mode, m.KXG08_ACCEL_ODR_NAVGA_MASK)
                self.set_bit(r.KXG08_ACCEL_ODR, b.KXG08_ACCEL_ODR_LPMODEA)                
            else:
                self.reset_bit(r.KXG08_ACCEL_ODR, b.KXG08_ACCEL_ODR_LPMODEA)     
        elif channel == CH_GYRO:        
            ## value validation
            assert lp_mode in e.KXG08_GYRO_ODR_NAVGG.values() or lp_mode == False, \
                'Invalid value for gyro low power mode. Valid values are: False or %s' % \
                e.KXG08_GYRO_ODR_NAVGG.keys()
            if lp_mode != False:
                self.set_bit_pattern(r.KXG08_GYRO_ODR, lp_mode, m.KXG08_GYRO_ODR_NAVGG_MASK)
                self.set_bit(r.KXG08_GYRO_ODR, b.KXG08_GYRO_ODR_LPMODEG)
            else:
                self.reset_bit(r.KXG08_GYRO_ODR, b.KXG08_GYRO_ODR_LPMODEG)  

    def set_BW(self, bw, channel = CH_ACC):                             # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]        
        if channel == CH_ACC:        
            assert bw in [b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, \
                          b.KXG08_ACCEL_CTL_ACC_BW_ODR_8]
            self.set_bit_pattern(r.KXG08_ACCEL_CTL, bw, m.KXG08_ACCEL_CTL_ACC_BW_MASK) 
        elif channel == CH_GYRO:
            assert bw in [b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, \
                            b.KXG08_GYRO_CTL_GYRO_BW_ODR_8]
            self.set_bit_pattern(r.KXG08_GYRO_CTL, bw, m.KXG08_GYRO_CTL_GYRO_BW_MASK)     

    def set_interrupt_polarity(self, intpin = 1, polarity = ACTIVE_LOW):
        assert intpin in self.INT_PINS
        assert polarity in [ACTIVE_LOW, ACTIVE_HIGH]

        if intpin == 1:
            if polarity == ACTIVE_LOW:
                self.set_bit_pattern(r.KXG08_INT_PIN_CTL, \
                                     b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW,
                                     m.KXG08_INT_PIN_CTL_IEA1_MASK)   # active low
            else:
                self.set_bit_pattern(r.KXG08_INT_PIN_CTL, \
                                     b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH,
                                     m.KXG08_INT_PIN_CTL_IEA1_MASK)# active high
        elif intpin == 2:
            if polarity == ACTIVE_LOW:
                self.set_bit_pattern(r.KXG08_INT_PIN_CTL, \
                                     b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW,
                                     m.KXG08_INT_PIN_CTL_IEA2_MASK)# active low
            else:
                self.set_bit_pattern(r.KXG08_INT_PIN_CTL, \
                                     b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH,
                                     m.KXG08_INT_PIN_CTL_IEA2_MASK)# active high
    
    def release_interrupts(self, intpin = 1):
        """ intpin are released separately """
        assert intpin in self.INT_PINS
        if intpin == 1:
            self.read_register(r.KXG08_INT1_L)
        elif intpin == 2:
            self.read_register(r.KXG08_INT2_L)

    def enable_fifo(self, mode = b.KXG08_BUF_EN_BUF_M_STREAM, axis_mask = 0x7F): # enable buffer with mode
        assert mode  in e.KXG08_BUF_EN_BUF_M.values()
        assert axis_mask <= 0x7F , 'temp, acc, gyro; max 7 axes possible set to storage '         

        self.write_register(r.KXG08_BUF_CTL1, axis_mask)        # buffer axes masks

        self.set_bit(r.KXG08_BUF_EN, b.KXG08_BUF_EN_BUFE)
        self.set_bit_pattern(r.KXG08_BUF_EN, mode, m.KXG08_BUF_EN_BUF_M_MASK)

    def disable_fifo(self):                                     # disable buffer
        self.reset_bit(r.KXG08_BUF_EN, b.KXG08_BUF_EN_BUFE)

    def get_fifo_resolution(self):                              # kxg07/8 has only 16b storage resolution
        assert "not implemented"

    def set_fifo_watermark_level(self, level, axes = 7):       # level is SAMPLE SETS
        ## level is datapackets (samples/ODR)
        assert axes <= 7, 'too many axes to store'
        assert level <= (4096 / (axes * 2)) ,'Watermark level too high.'
        lsb = (level & 0b00001111) << 4
        msb = level >> 4
        self.write_register(r.KXG08_BUF_WMITH_L, lsb)           
        self.write_register(r.KXG08_BUF_WMITH_H, msb)

    def get_fifo_level(self):                                   # Hox! get fifo buffer BYTE level
        ## buffer level          
        sample_in_buffer_l = self.read_register(r.KXG08_BUF_SMPLEV_L)[0]
        sample_in_buffer_h = self.read_register(r.KXG08_BUF_SMPLEV_H)[0]
        
        sample_in_buffer = (sample_in_buffer_h << 4)
        sample_in_buffer |= (sample_in_buffer_l >> 4)
        return sample_in_buffer 

    def clear_buffer(self):
        self.write_register(r.KXG08_BUF_CLEAR, 0xff)

    def wake_sleep(self, mode):                                   # select wake or sleep mode manually
        assert mode in [SLEEP, WAKE]
        if mode == WAKE:
            self.set_bit(r.KXG08_WAKE_SLEEP_CTL2, b.KXG08_WAKE_SLEEP_CTL2_MAN_WAKE)
            # wait until wake setup bit released 
            while self.read_register(r.KXG08_WAKE_SLEEP_CTL2, 1)[0] & b.KXG08_WAKE_SLEEP_CTL2_MAN_WAKE <> 0: pass
            # wait until wake mode valid
            while self.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_WAKE_SLEEP_WAKE_MODE == 0: pass
            return
        elif mode == SLEEP:
            self.set_bit(r.KXG08_WAKE_SLEEP_CTL2, b.KXG08_WAKE_SLEEP_CTL2_MAN_SLEEP)
            # wait until sleep setup bit released
            while self.read_register(r.KXG08_WAKE_SLEEP_CTL2, 1)[0] & b.KXG08_WAKE_SLEEP_CTL2_MAN_SLEEP <> 0: pass
            # wait until sleep mode valid
            while self.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_WAKE_SLEEP_SLEEP_MODE > 0: pass
            return
        assert 0, "wrong wake/sleep mode"

def directions(dir):            # print wuf+bts source directions
    fst = True
    pos = ""
    for i in range(0, 6):
        mask = 0x01 << i
        if dir & mask > 0:
            if not fst:
                pos = pos + "+" + wufbts_direction[dir & mask]
            else:
                pos = wufbts_direction[dir & mask]
                fst = False
    return pos
