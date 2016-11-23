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
from lib.sensor_base import sensor_base, SensorException

import kxg03_registers as sensor
r = sensor.registers()
b = sensor.bits()
m = sensor.masks()

class kxg03_driver(sensor_base):
    _WAIS   = [b.KXG03_WHO_AM_I_WIA_ID, 0xED]  # 0xed is temporary id

    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x4E, 0x4F] 
        self.SPI_SUPPORT = True
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.KXG03_WAKE_CNT_L, r.KXG03_BUF_STATUS)

    def probe(self):
        """
        Read sensor ID register and make sure value is expected one. Return 1 if ID is correct.
        """
        resp = self.read_register(r.KXG03_WHO_AM_I)
        if resp[0] in self._WAIS:
            self.WHOAMI = resp[0]
            logger.info('kxg03 found')
            return 1
        logger.warning("wrong WHOAMI received for kxg03: 0x%02x" % resp[0])
        return 0

    def por(self):
        self.write_register(r.KXG03_CTL_REG_1, b.KXG03_CTL_REG_1_RST)
        logger.debug("wait POR"),
        timeout = 100
        while timeout > 0:
            timeout = timeout - 1
            if (self.read_register(r.KXG03_STATUS1, 1)[0] & b.KXG03_STATUS1_POR):
                logger.debug("POR done")
                break                                           # POR done
        if timeout == 0:
            raise SensorException('POR failure')
        
    def set_power_on(self, channel = CH_ACC):                   # set sleep and wake modes ON
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel    
        if channel & CH_ACC > 0:
            self.set_bit_pattern(r.KXG03_STDBY,             b.KXG03_STDBY_ACC_STDBY_ENABLED, \
                                                            m.KXG03_STDBY_ACC_STDBY_MASK)
        if channel & CH_GYRO > 0:
            self.set_bit_pattern(r.KXG03_STDBY,   b.KXG03_STDBY_GYRO_STDBY_S_ENABLED, \
                                                  m.KXG03_STDBY_GYRO_STDBY_S_MASK)
            self.set_bit_pattern(r.KXG03_STDBY,   b.KXG03_STDBY_GYRO_STDBY_W_ENABLED, \
                                                  m.KXG03_STDBY_GYRO_STDBY_W_MASK)
            ## wait gyro start
            timeout = 200
            while timeout > 0 :                 # wait for gyro running
                stat = self.read_register(r.KXG03_STATUS1, 1)[0]
                timeout = timeout - 1
                if stat & b.KXG03_STATUS1_GYRO_RUN:
                    break
          
            if timeout < 1:
                raise SensorException('start failure')

        if channel & CH_TEMP > 0:
            self.set_bit_pattern(r.KXG03_CTL_REG_1,         b.KXG03_CTL_REG_1_TEMP_STDBY_S_ENABLED,
                                                            m.KXG03_CTL_REG_1_TEMP_STDBY_S_MASK)
            self.set_bit_pattern(r.KXG03_CTL_REG_1,         b.KXG03_CTL_REG_1_TEMP_STDBY_W_ENABLED,
                                                            m.KXG03_CTL_REG_1_TEMP_STDBY_W_MASK)

    def set_power_off(self, channel = CH_ACC | CH_GYRO | CH_TEMP):  # set sleep and wake modes OFF
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel
        if channel & CH_ACC > 0:
            self.set_bit(r.KXG03_STDBY,             b.KXG03_STDBY_ACC_STDBY_DISABLED)
        if channel & CH_TEMP > 0:
            self.set_bit(r.KXG03_CTL_REG_1,         b.KXG03_CTL_REG_1_TEMP_STDBY_S_DISABLED)
            self.set_bit(r.KXG03_CTL_REG_1,         b.KXG03_CTL_REG_1_TEMP_STDBY_W_DISABLED)
        if channel & CH_GYRO > 0:
            self.set_bit(r.KXG03_STDBY,             b.KXG03_STDBY_GYRO_STDBY_S_DISABLED) 
            self.set_bit(r.KXG03_STDBY,             b.KXG03_STDBY_GYRO_STDBY_W_DISABLED)            

    def read_data(self, channel = CH_ACC | CH_GYRO ):
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel
        s_form = ()
        if channel & CH_TEMP > 0:
            data = self.read_register(r.KXG03_TEMP_OUT_L, 2)
            s_form = s_form + struct.unpack('h', data)
        if channel & CH_GYRO > 0:
            data = self.read_register(r.KXG03_GYRO_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        if channel & CH_ACC > 0:
            data = self.read_register(r.KXG03_ACC_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        return s_form

    def read_drdy(self, intpin=1, channel = CH_ACC):            # separated interrupt sources
        assert channel in [CH_ACC, CH_GYRO]
        assert intpin in self.INT_PINS
        if intpin == 1:
            ins1 = self.read_register(r.KXG03_INT1_SRC1)[0]
            if channel & CH_ACC > 0:        
                return ins1 & b.KXG03_INT1_SRC1_INT1_DRDY_ACCTEMP != 0
            if channel & CH_GYRO > 0:
                return ins1 & b.KXG03_INT1_SRC1_INT1_DRDY_GYRO != 0
        if intpin == 2:
            ins2 = self.read_register(r.KXG03_INT2_SRC1)[0]
            if channel & CH_ACC > 0:
                return ins2 & b.KXG03_INT2_SRC1_INT2_DRDY_ACCTEMP != 0
            if channel & CH_GYRO > 0:
                return ins2 & b.KXG03_INT2_SRC1_INT2_DRDY_GYRO != 0          

    def set_default_on(self):
        "ACC+GYRO+temp: 2g/25Hz/, 256dps/25Hz, drdy (ACC) INT1, sleep and wake modes"
        self.set_odr(b.KXG03_ACCEL_ODR_WAKE_ODRA_W_25, \
                     b.KXG03_ACCEL_ODR_SLEEP_ODRA_S_25, CH_ACC)         # wake and sleep
        self.set_odr(b.KXG03_GYRO_ODR_WAKE_ODRG_W_25, \
                     b.KXG03_GYRO_ODR_SLEEP_ODRG_S_25, CH_GYRO)        # wake and sleep
        
        self.set_range(b.KXG03_ACCEL_CTL_ACC_FS_W_2G, \
                       b.KXG03_ACCEL_CTL_ACC_FS_S_2G, CH_ACC)           # wake and sleep
        self.set_range(b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_256, \
                       b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_256, CH_GYRO)   # wake and sleep

        ## averaging for acc and BW for gyro
        self.set_average(b.KXG03_ACCEL_ODR_WAKE_NAVG_W_128_SAMPLE_AVG, \
                         b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_2_SAMPLE_AVG, CH_ACC) # only in low power mode, for wake and sleep modes
        self.set_BW(b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_10, \
                    b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_10, CH_GYRO)     # wake and sleep

        ## interrupts not set
        self.write_register(r.KXG03_INT_PIN1_SEL, 0)                  # routing 0
        self.write_register(r.KXG03_INT_MASK1, 0)                     # mask 0       
        self.write_register(r.KXG03_INT_PIN2_SEL, 0)                  # routing 0
        ## interrupt settings
        self.write_register(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN1            | \
                                                 b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_LOW | \
                                                 b.KXG03_INT_PIN_CTL_IEL1_LATCHED)

        self.enable_drdy(1, CH_ACC)                                     # acc drdy, physical int
        #self.enable_drdy(1, CH_GYRO)                                    # gyro drdy, physical int

        self.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)                   # all sensors ON

    def enable_drdy(self, intpin=1, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        assert intpin in self.INT_PINS
        if( (channel & CH_ACC) > 0):
            #enable data ready
            self.set_bit(r.KXG03_INT_MASK1,         b.KXG03_INT_MASK1_DRDY_ACCTEMP)

            # route data ready to pin
            if intpin == 1:
                self.set_bit(r.KXG03_INT_PIN1_SEL,  b.KXG03_INT_PIN1_SEL_DRDY_ACCTEMP_P1)
            else:
                self.set_bit(r.KXG03_INT_PIN2_SEL,  b.KXG03_INT_PIN2_SEL_DRDY_ACCTEMP_P2)
                
        if( (channel & CH_GYRO) > 0):
            self.set_bit(r.KXG03_INT_MASK1,         b.KXG03_INT_MASK1_DRDY_GYRO)            
            if intpin == 1:
                self.set_bit(r.KXG03_INT_PIN1_SEL,  b.KXG03_INT_PIN1_SEL_DRDY_GYRO_P1)
            else:
                self.set_bit(r.KXG03_INT_PIN2_SEL,  b.KXG03_INT_PIN2_SEL_DRDY_GYRO_P2) 

    def disable_drdy(self, intpin=1, channel = CH_ACC):         # set separately for acc or gyro
        assert channel in [CH_ACC ,CH_GYRO]
        assert intpin in self.INT_PINS
        if channel & CH_ACC > 0:
            self.reset_bit(r.KXG03_INT_MASK1, b.KXG03_INT_MASK1_DRDY_ACCTEMP)
            if intpin == 1:
                self.reset_bit(r.KXG03_INT_PIN1_SEL, b.KXG03_INT_PIN1_SEL_DRDY_ACCTEMP_P1)
            else:
                self.reset_bit(r.KXG03_INT_PIN2_SEL, b.KXG03_INT_PIN2_SEL_DRDY_ACCTEMP_P2)                                     
        if channel & CH_GYRO > 0:
            self.reset_bit(r.KXG03_INT_MASK1, b.KXG03_INT_MASK1_DRDY_GYRO)            
            if intpin == 1:
                self.reset_bit(r.KXG03_INT_PIN1_SEL, b.KXG03_INT_PIN1_SEL_DRDY_GYRO_P1)
            else:
                self.reset_bit(r.KXG03_INT_PIN2_SEL, b.KXG03_INT_PIN2_SEL_DRDY_GYRO_P2) 

    def set_odr(self, ODR_W, ODR_S, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        if channel & CH_ACC > 0:        
            self.set_bit_pattern(r.KXG03_ACCEL_ODR_WAKE,  ODR_W, \
                                                          m.KXG03_ACCEL_ODR_WAKE_ODRA_W_MASK)
            self.set_bit_pattern(r.KXG03_ACCEL_ODR_SLEEP, ODR_S, \
                                                          m.KXG03_ACCEL_ODR_SLEEP_ODRA_S_MASK)
        if channel & CH_GYRO > 0:
            self.set_bit_pattern(r.KXG03_GYRO_ODR_WAKE,  ODR_W, \
                                                          m.KXG03_GYRO_ODR_WAKE_ODRG_W_MASK)
            self.set_bit_pattern(r.KXG03_GYRO_ODR_SLEEP, ODR_S, \
                                                          m.KXG03_GYRO_ODR_SLEEP_ODRG_S_MASK)

    def set_range(self, range_W, range_S, channel = CH_ACC):    # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]        
        if channel & CH_ACC > 0:
            assert (range_W | range_S) in [b.KXG03_ACCEL_CTL_ACC_FS_W_2G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_W_4G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_W_8G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_W_16G,\
                                           b.KXG03_ACCEL_CTL_ACC_FS_S_2G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_S_4G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_S_8G, \
                                           b.KXG03_ACCEL_CTL_ACC_FS_S_16G]
            self.set_bit_pattern(r.KXG03_ACCEL_CTL, range_W, m.KXG03_ACCEL_CTL_ACC_FS_W_MASK)
            self.set_bit_pattern(r.KXG03_ACCEL_CTL, range_S, m.KXG03_ACCEL_CTL_ACC_FS_S_MASK)
        if channel & CH_GYRO > 0:
            assert (range_W | range_S) in [b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_256, \
                                           b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_512, \
                                           b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_1024,\
                                           b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_2048,\
                                           b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_256, \
                                           b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_512, \
                                           b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_1024,\
                                           b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_2048]            
            self.set_bit_pattern(r.KXG03_GYRO_ODR_WAKE, range_W, m.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_MASK)
            self.set_bit_pattern(r.KXG03_GYRO_ODR_WAKE, range_S, m.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_MASK)

    def set_average(self, average_W, average_S, channel = CH_ACC):                  # oversampling setting for low power mode
        assert channel in [CH_ACC, CH_GYRO]          
        assert (average_W) in [b.KXG03_ACCEL_ODR_WAKE_NAVG_W_128_SAMPLE_AVG,\
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_64_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_32_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_16_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_8_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_4_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_2_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_WAKE_NAVG_W_NO_AVG]

        assert (average_S) in [b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_128_SAMPLE_AVG,
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_64_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_32_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_16_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_8_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_4_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_2_SAMPLE_AVG,  \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_NO_AVG]      
        if channel & CH_ACC > 0: # only acc for kxg03
            self.set_bit_pattern(r.KXG03_ACCEL_ODR_WAKE,  average_W, m.KXG03_ACCEL_ODR_WAKE_NAVG_W_MASK)
            self.set_bit_pattern(r.KXG03_ACCEL_ODR_SLEEP, average_S, m.KXG03_ACCEL_ODR_SLEEP_NAVG_S_MASK)

    def set_BW(self, reso_W, reso_S, channel = CH_GYRO):
        assert channel in [CH_GYRO], 'BW limitter control only for gyro sensor'
        if channel & CH_GYRO > 0:
            assert (reso_W | reso_S) in [b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_10, \
                                         b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_20, \
                                         b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_40, \
                                         b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_160,\
                                         b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_10, \
                                         b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_20, \
                                         b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_40, \
                                         b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_160]
            self.set_bit_pattern(r.KXG03_GYRO_ODR_WAKE,  reso_W, m.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_MASK)
            self.set_bit_pattern(r.KXG03_GYRO_ODR_SLEEP, reso_S, m.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_MASK)

    def release_interrupts(self, intpin=1):
        """ intpin are released separately """ 
        assert intpin in self.INT_PINS
        if intpin == 1:
            self.read_register(r.KXG03_INT1_L)
        else:
            self.read_register(r.KXG03_INT2_L)
            
    def enable_fifo(self, mode = b.KXG03_BUF_EN_BUF_M_STREAM, res=16, axis_mask=0x7F): # enable buffer with mode
        ### syncronized with KXxxx, KXG03
        assert mode <= 4, 'wrong buffer model'
        assert res == 16, 'buffer storage of KXG03 has only 16b resolution supported'
        assert axis_mask <= 0x7F , 'temp, acc, gyro; max 7 axes possible set to storage '

        ## both modes set same way 
        self.set_bit(r.KXG03_BUF_CTL2, axis_mask)       # wake mode
        self.set_bit(r.KXG03_BUF_CTL3, axis_mask)       # sleep mode
        
        self.set_bit(r.KXG03_BUF_EN, b.KXG03_BUF_EN_BUFE)
        self.set_bit_pattern(r.KXG03_BUF_EN, mode, m.KXG03_BUF_EN_BUF_M_MASK)

    def disable_fifo(self):                                     # disable buffer
        self.reset_bit(r.KXG03_BUF_EN, b.KXG03_BUF_EN_BUFE)

    def set_fifo_watermark_level(self, level, axes = 7):        #
        ### syncronized with KXxxx, KXG03
        ## level is datapackets       
        assert axes <= 7, 'too many axes to store'
        assert level <= (1024 / (axes * 2)) ,'Watermark level too high.'
        lsb = (level & 0x03) << 6
        msb = level >> 2
        
        self.write_register(r.KXG03_BUF_WMITH_L, lsb)           
        self.write_register(r.KXG03_BUF_WMITH_H, msb
                            )
    def get_fifo_level(self):                                   # Hox! get fifo buffer BYTE level
        ## buffer level            
        sample_in_buffer_l = self.read_register(r.KXG03_BUF_SMPLEV_L)[0]
        sample_in_buffer_h = self.read_register(r.KXG03_BUF_SMPLEV_H)[0]
        
        sample_in_buffer = (sample_in_buffer_h << 2)
        sample_in_buffer |= (sample_in_buffer_l >> 6)
        
        return sample_in_buffer 

    def clear_buffer(self):
        self.write_register(r.KXG03_BUF_CLEAR, 0xff)        
    
##
##
## utility functions
##
##

## common functinality for sensor tests
LPMODE, FULL_RES  = range(2)
SLEEP, WAKE = range(2)

## wuf and bts_directions
wufbts_direction = {
   b.KXG03_INT1_SRC2_INT1_ZNWU : "FACE_UP",
   b.KXG03_INT1_SRC2_INT1_ZPWU : "FACE_DOWN",
   b.KXG03_INT1_SRC2_INT1_XNWU : "UP",
   b.KXG03_INT1_SRC2_INT1_XPWU : "DOWN",
   b.KXG03_INT1_SRC2_INT1_YPWU : "RIGHT",
   b.KXG03_INT1_SRC2_INT1_YNWU : "LEFT" }

def power_modes(sensor, RES, MODE):                 #  defines accelerometer power modes for wake and sleep
    if RES == LPMODE and MODE == SLEEP:      
        sensor.set_bit_pattern(r.KXG03_ACCEL_ODR_SLEEP, b.KXG03_ACCEL_ODR_SLEEP_LPMODE_S_ENABLED, \
                                                        m.KXG03_ACCEL_ODR_SLEEP_LPMODE_S_MASK)
    elif RES == LPMODE and MODE == WAKE:      
        sensor.set_bit_pattern(r.KXG03_ACCEL_ODR_WAKE,  b.KXG03_ACCEL_ODR_WAKE_LPMODE_W_ENABLED, \
                                                        m.KXG03_ACCEL_ODR_WAKE_LPMODE_W_MASK)
    elif RES == FULL_RES and MODE == SLEEP:
        sensor.set_bit_pattern(r.KXG03_ACCEL_ODR_SLEEP, b.KXG03_ACCEL_ODR_SLEEP_LPMODE_S_DISABLED, \
                                                        m.KXG03_ACCEL_ODR_SLEEP_LPMODE_S_MASK)
    elif RES == FULL_RES and MODE == WAKE:
        sensor.set_bit_pattern(r.KXG03_ACCEL_ODR_WAKE,  b.KXG03_ACCEL_ODR_WAKE_LPMODE_W_DISABLED, \
                                                        m.KXG03_ACCEL_ODR_WAKE_LPMODE_W_MASK)
    else:
        assert 0,'unknown combination'

def wake_sleep(sensor, mode):                           # select wake or sleep mode manually
    assert mode in [SLEEP, WAKE]
    if mode == WAKE:
        sensor.set_bit(r.KXG03_WAKE_SLEEP_CTL1, b.KXG03_WAKE_SLEEP_CTL1_MAN_WAKE)
        # wait until wake setup bit released 
        while sensor.read_register(r.KXG03_WAKE_SLEEP_CTL1, 1)[0] & b.KXG03_WAKE_SLEEP_CTL1_MAN_WAKE: pass
        # wait until wake mode valid
        while sensor.read_register(r.KXG03_STATUS1, 1)[0] & b.KXG03_STATUS1_WAKE_SLEEP_WAKE_MODE == 0: pass
    else:
        sensor.set_bit(r.KXG03_WAKE_SLEEP_CTL1, b.KXG03_WAKE_SLEEP_CTL1_MAN_SLEEP)
        # wait until sleep setup bit released
        while sensor.read_register(r.KXG03_WAKE_SLEEP_CTL1, 1)[0] & b.KXG03_WAKE_SLEEP_CTL1_MAN_SLEEP: pass
        # wait until sleep mode valid
        while sensor.read_register(r.KXG03_STATUS1, 1)[0] & b.KXG03_STATUS1_WAKE_SLEEP_SLEEP_MODE > 0: pass

    assert "wrong wake/sleep mode"
    
def directions(dir):            # print wuf+bts source directions
    fst = True
    pos = None
    for i in range(0, 6):
        mask = 0x01 << i
        if dir & mask > 0:
            if not fst:
                pos = pos + "+" + wufbts_direction[dir & mask]
            else:
                pos = wufbts_direction[dir & mask]
                fst = False
    return pos

def wait_drdy_reg(sensor, intpin, channel=CH_ACC):
    ## poll DRDY register (acc or gyro) for test polling communication capability
    count = 0
    if channel == CH_ACC:                                           # release drdy bit just in case
        data = sensor.read_register(r.KXG03_ACC_XOUT_L, 1)[0]       # acc releases drdy latch
    else:
        data = sensor.read_register(r.KXG03_GYRO_XOUT_L, 1)[0]      # gyro releases drdy latch
    while not sensor.read_drdy(intpin, channel): pass               # wait until next sample is ready
    while sensor.read_drdy(intpin, channel):                        # wait until sample ready and release drdy bit
        if channel == CH_ACC:
            data = sensor.read_register(r.KXG03_ACC_XOUT_L, 1)[0]   # acc releases drdy latch
        else:
            data = sensor.read_register(r.KXG03_GYRO_XOUT_L, 1)[0]  # gyro releases drdy latch
    while not sensor.read_drdy(intpin, channel):                    # finally wait beginning of drdy not ready (transition edge)
        count += 1
    assert count > 0,'Data overflow. Maybe ODR is too high for host adapter'

