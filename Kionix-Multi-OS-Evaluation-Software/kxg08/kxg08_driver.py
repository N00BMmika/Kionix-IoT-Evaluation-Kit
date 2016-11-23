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

import kxg08_registers as sensor
r = sensor.registers()
b = sensor.bits()
m = sensor.masks()

class kxg08_driver(sensor_base):
    _WAIS   = [b.KXG08_WHO_AM_I_WIA_ID,
               b.KXG08_2080_WHO_AM_I_WIA_ID,
               b.KXG07_WHO_AM_I_WIA_ID,
               b.KXG07_2080_WHO_AM_I_WIA_ID,
               0x04
              ] ## 0x04 is temporary ID
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
            elif self.WHOAMI == b.KXG08_2080_WHO_AM_I_WIA_ID:
                logger.info('kxg08-2080 found')
            elif self.WHOAMI == b.KXG07_WHO_AM_I_WIA_ID:                
                logger.info('kxg07-1080 found')
            elif self.WHOAMI == b.KXG07_2080_WHO_AM_I_WIA_ID:                
                logger.info('kxg07-2080 found')                
            else:
                logger.info("other valid WHOAMI received 0x%02x" % resp[0])
            return 1
        logger.debug("wrong WHOAMI received 0x%02x" % resp[0])
        return 0

    def por(self):
        self.write_register(r.KXG08_CTL_REG_1, b.KXG08_CTL_REG_1_SRST)
        logger.debug("Soft Reset")
        timeout = 100
        while timeout > 0:
            timeout = timeout - 1            
            if (self.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_POR):
                logger.debug("POR done")
                break                                           # POR done
        if timeout == 0:
            raise SensorException('POR failure')
            
    def set_power_on(self, channel = CH_ACC):                   # set sleep and wake modes ON
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel    
        if channel & CH_ACC > 0:
            self.set_bit_pattern(r.KXG08_STDBY, b.KXG08_STDBY_ACC_STDBY_ENABLED, \
                                                m.KXG08_STDBY_ACC_STDBY_MASK)
            acc_odr = self.read_register(r.KXG08_ACCEL_ODR,1)[0] & m.KXG08_ACCEL_ODR_ODRA_MASK
            acc_start_delay = 1 / (2**acc_odr * 0.78125) *1.55
            time.sleep(acc_start_delay)
            
        if channel & CH_GYRO > 0:
            self.set_bit_pattern(r.KXG08_STDBY, b.KXG08_STDBY_GYRO_STDBY_ENABLED | b.KXG08_STDBY_GYRO_FSTART_DISABLED, \
                                                m.KXG08_STDBY_GYRO_STDBY_MASK | m.KXG08_STDBY_GYRO_FSTART_MASK)
            time.sleep(1)
            logger.debug("wait gyro start")
            timeout = 100
            while timeout > 0:                                       # wait for gyro running
                stat = self.read_register(r.KXG08_STATUS1, 1)[0]
                timeout = timeout - 1
                if stat & b.KXG08_STATUS1_GYRO_RUN:
                    break
    
            if timeout == 0:
                raise SensorException('start failure')

        if channel & CH_TEMP > 0:
            self.reset_bit(r.KXG08_STDBY, b.KXG08_STDBY_TEMP_STDBY_DISABLED)

    def set_power_off(self, channel = CH_ACC | CH_GYRO | CH_TEMP):  # set sleep and wake modes OFF
        assert channel & (CH_ACC | CH_GYRO | CH_TEMP) == channel
        if channel & CH_ACC > 0:
            self.set_bit(r.KXG08_STDBY, b.KXG08_STDBY_ACC_STDBY_DISABLED) 
        if channel & CH_TEMP > 0:
            self.set_bit(r.KXG08_STDBY, b.KXG08_STDBY_TEMP_STDBY_DISABLED)
        if channel & CH_GYRO > 0:
            self.set_bit(r.KXG08_STDBY, b.KXG08_STDBY_GYRO_FSTART_DISABLED)                     

    def read_data(self, channel = CH_ACC):
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
        "ACC+GYRO+temp: 2g/25Hz/128s, 256dps/100Hz/10Hz"
        self.set_odr(b.KXG08_ACCEL_ODR_ODRA_25, 0, CH_ACC)          # acc
        self.set_odr(b.KXG08_GYRO_ODR_ODRG_100, 0, CH_GYRO)         # gyro
        
        self.set_range(b.KXG08_ACCEL_CTL_ACC_FS_2G, 0, CH_ACC)      # acc
        self.set_range(b.KXG08_GYRO_CTL_GYRO_FS_256, 0, CH_GYRO)    # gyro

        self.set_average(b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG, CH_ACC) # acc average
        self.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, CH_ACC)         # acc BW
        ##### self.set_average(b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG, CH_GYRO) # gyro average (only for 2080 version        
        self.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, CH_GYRO)        # gyro BW

        self.write_register(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH  | \
                                                 b.KXG08_INT_PIN_CTL_IEL2_LATCHED      | \
                                                 b.KXG08_INT_PIN_CTL_IEN1              | \
                                                 b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH  | \
                                                 b.KXG08_INT_PIN_CTL_IEL1_LATCHED)
        self.enable_drdy(2, CH_ACC)                                     # acc drdy, physical int2
        #self.enable_drdy(2, CH_GYRO)                                   # gyro drdy, physical int1

        self.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)                   # all sensors ON

    def enable_drdy(self, intpin=1, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        assert intpin in self.INT_PINS
        if( (channel & CH_ACC) > 0):
            #enable data ready function
            self.set_bit(r.KXG08_INT_MASK1,         b.KXG08_INT_MASK1_DRDY_ACC)
            
            # route data ready to pin
            if intpin == 1:
                self.set_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_ACC_P1)
            else:
                self.set_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_ACC_P2)
                
        if( (channel & CH_GYRO) > 0):
            self.set_bit(r.KXG08_INT_MASK1,         b.KXG08_INT_MASK1_DRDY_GYRO)            
            if intpin == 1:
                self.set_bit(r.KXG08_INT_PIN_SEL1,  b.KXG08_INT_PIN_SEL1_DRDY_GYRO_P1)
            else:
                self.set_bit(r.KXG08_INT_PIN_SEL2,  b.KXG08_INT_PIN_SEL2_DRDY_GYRO_P2) 

    def disable_drdy(self, intpin=1, channel = CH_ACC):         # set separately for acc or gyro
        assert channel in [CH_ACC ,CH_GYRO]
        assert intpin in self.INT_PINS
        if channel & CH_ACC > 0:
            self.reset_bit(r.KXG08_INT_MASK1, b.KXG08_INT_MASK1_DRDY_ACC)          
            if intpin == 1:
                self.reset_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_ACC_P1)
            else:
                self.reset_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_ACC_P2)
        if channel & CH_GYRO > 0:
            self.reset_bit(r.KXG08_INT_MASK1, b.KXG08_INT_MASK1_DRDY_GYRO)
            if intpin == 1:
                self.reset_bit(r.KXG08_INT_PIN_SEL1, b.KXG08_INT_PIN_SEL1_DRDY_GYRO_P1)
            else:
                self.reset_bit(r.KXG08_INT_PIN_SEL2, b.KXG08_INT_PIN_SEL2_DRDY_GYRO_P2)

    def set_odr(self, odr, ordx = None, channel = CH_ACC):          # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]
        if channel & CH_ACC > 0:        
            self.set_bit_pattern(r.KXG08_ACCEL_ODR, odr, m.KXG08_ACCEL_ODR_ODRA_MASK)

        if channel & CH_GYRO > 0:
            self.set_bit_pattern(r.KXG08_GYRO_ODR, odr, m.KXG08_GYRO_ODR_ODRG_MASK)

    def set_range(self, range, rangex = None, channel = CH_ACC):    # set separately for acc or gyro
        assert channel in [CH_ACC, CH_GYRO]        
        if channel & CH_ACC > 0:
            assert range in [b.KXG08_ACCEL_CTL_ACC_FS_2G, \
                             b.KXG08_ACCEL_CTL_ACC_FS_4G, \
                             b.KXG08_ACCEL_CTL_ACC_FS_8G, \
                             b.KXG08_ACCEL_CTL_ACC_FS_16G]
            self.set_bit_pattern(r.KXG08_ACCEL_CTL, range, m.KXG08_ACCEL_CTL_ACC_FS_MASK)
            
        if channel & CH_GYRO > 0:
            assert range in [b.KXG08_GYRO_CTL_GYRO_FS_64,  \
                             b.KXG08_GYRO_CTL_GYRO_FS_128, \
                             b.KXG08_GYRO_CTL_GYRO_FS_256, \
                             b.KXG08_GYRO_CTL_GYRO_FS_512, \
                             b.KXG08_GYRO_CTL_GYRO_FS_1024,\
                             b.KXG08_GYRO_CTL_GYRO_FS_2048]            
            self.set_bit_pattern(r.KXG08_GYRO_CTL, range, m.KXG08_GYRO_CTL_GYRO_FS_MASK)

    ## sets low power mode AND averaging factor
    def set_average(self, average, averagex = None, channel = CH_ACC):        # oversampling setting for low power mode
        assert channel in [CH_ACC, CH_GYRO]        
        if channel & CH_ACC > 0:        
            assert average in [b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG,\
                            b.KXG08_ACCEL_ODR_NAVGA_64_SAMPLE_AVG, \
                            b.KXG08_ACCEL_ODR_NAVGA_32_SAMPLE_AVG, \
                            b.KXG08_ACCEL_ODR_NAVGA_16_SAMPLE_AVG, \
                            b.KXG08_ACCEL_ODR_NAVGA_8_SAMPLE_AVG,  \
                            b.KXG08_ACCEL_ODR_NAVGA_4_SAMPLE_AVG,  \
                            b.KXG08_ACCEL_ODR_NAVGA_2_SAMPLE_AVG,  \
                            b.KXG08_ACCEL_ODR_NAVGA_NO_AVG]            
            self.set_bit_pattern(r.KXG08_ACCEL_ODR, average, m.KXG08_ACCEL_ODR_NAVGA_MASK)
        if channel & CH_GYRO > 0:        
            assert average in [b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG,\
                            b.KXG08_GYRO_ODR_NAVGG_64_SAMPLE_AVG, \
                            b.KXG08_GYRO_ODR_NAVGG_32_SAMPLE_AVG, \
                            b.KXG08_GYRO_ODR_NAVGG_16_SAMPLE_AVG, \
                            b.KXG08_GYRO_ODR_NAVGG_8_SAMPLE_AVG,  \
                            b.KXG08_GYRO_ODR_NAVGG_4_SAMPLE_AVG,  \
                            b.KXG08_GYRO_ODR_NAVGG_2_SAMPLE_AVG,  \
                            b.KXG08_GYRO_ODR_NAVGG_NO_AVG]
            self.set_bit_pattern(r.KXG08_GYRO_ODR, average, m.KXG08_GYRO_ODR_NAVGG_MASK)

    def set_BW(self, bw, channel = CH_ACC):
        assert channel in [CH_ACC, CH_GYRO]        
        if channel & CH_ACC > 0:        
            assert bw in [b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, \
                          b.KXG08_ACCEL_CTL_ACC_BW_ODR_8]
            self.set_bit_pattern(r.KXG08_ACCEL_CTL, bw, m.KXG08_ACCEL_CTL_ACC_BW_MASK) 
        if channel & CH_GYRO > 0:
            assert bw in [b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, \
                            b.KXG08_GYRO_CTL_GYRO_BW_ODR_8]
            self.set_bit_pattern(r.KXG08_GYRO_CTL, bw, m.KXG08_GYRO_CTL_GYRO_BW_MASK)           

    def release_interrupts(self, intpin = 1):
        """ intpin are released separately """
        assert intpin in self.INT_PINS
        if intpin == 1:
            self.read_register(r.KXG08_INT1_L)
        else:
            self.read_register(r.KXG08_INT2_L)

    def enable_fifo(self, mode = b.KXG08_BUF_EN_BUF_M_STREAM, res = None, axis_mask = 0x7F): # enable buffer with mode
        assert mode < 4
        assert axis_mask <= 0x7F , 'temp, acc, gyro; max 7 axes possible set to storage '         

        self.set_bit(r.KXG08_BUF_CTL1, axis_mask)       # buffer axes masks
        
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
        self.write_register(r.KXG08_BUF_CLEAR, 0)

   
## common functinality for sensor tests
LPMODE, FULL_RES  = range(2)
SLEEP, WAKE = range(2)

## wuf and bts_directions
wufbts_direction = {
   b.KXG08_INT1_SRC2_INT1_ZNWU : "FACE_UP",
   b.KXG08_INT1_SRC2_INT1_ZPWU : "FACE_DOWN",
   b.KXG08_INT1_SRC2_INT1_XNWU : "UP",
   b.KXG08_INT1_SRC2_INT1_XPWU : "DOWN",
   b.KXG08_INT1_SRC2_INT1_YPWU : "RIGHT",
   b.KXG08_INT1_SRC2_INT1_YNWU : "LEFT" }

### KXG07/8 has no separate powerlevel SLEEP mode settings
def power_modes(sensor, res, mode = None, channel = CH_ACC):    # defines power modes
    assert channel & (CH_ACC | CH_GYRO) == channel
    assert res in [LPMODE, FULL_RES]
    if channel & CH_ACC > 0:        
        if res == LPMODE:      
            sensor.set_bit(r.KXG08_ACCEL_ODR, b.KXG08_ACCEL_ODR_LPMODEA)
        elif res == FULL_RES:
            sensor.reset_bit(r.KXG08_ACCEL_ODR, b.KXG08_ACCEL_ODR_LPMODEA)
    if channel & CH_GYRO > 0:                                   # defines gyro's power modes, only for 2080 version
        if res == LPMODE:        
            sensor.set_bit(r.KXG08_GYRO_ODR, b.KXG08_GYRO_ODR_LPMODEG)
        elif res == FULL_RES:
            sensor.reset_bit(r.KXG08_GYRO_ODR, b.KXG08_GYRO_ODR_LPMODEG)

def wake_sleep(sensor, mode):                                   # select wake or sleep mode manually
    assert mode in [SLEEP, WAKE]
    if mode == WAKE:
        sensor.set_bit(r.KXG08_WAKE_SLEEP_CTL2, b.KXG08_WAKE_SLEEP_CTL2_MAN_WAKE)
        # wait until wake setup bit released 
        while sensor.read_register(r.KXG08_WAKE_SLEEP_CTL2, 1)[0] & b.KXG08_WAKE_SLEEP_CTL2_MAN_WAKE <> 0: pass
        # wait until wake mode valid
        while sensor.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_WAKE_SLEEP_WAKE_MODE == 0: pass
        return
    elif mode == SLEEP:
        sensor.set_bit(r.KXG08_WAKE_SLEEP_CTL2, b.KXG08_WAKE_SLEEP_CTL2_MAN_SLEEP)
        # wait until sleep setup bit released
        while sensor.read_register(r.KXG08_WAKE_SLEEP_CTL2, 1)[0] & b.KXG08_WAKE_SLEEP_CTL2_MAN_SLEEP <> 0: pass
        # wait until sleep mode valid
        while sensor.read_register(r.KXG08_STATUS1, 1)[0] & b.KXG08_STATUS1_WAKE_SLEEP_SLEEP_MODE > 0: pass
        return

    assert 0, "wrong wake/sleep mode"
    
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
    ## poll DRDY register (acc or gyro) for test communication capability
    count = 0
    if channel == CH_ACC:                                           # release drdy bit just in case
        data = sensor.read_register(r.KXG08_ACCEL_XOUT_L, 1)[0]       # acc releases drdy latch
    else:
        data = sensor.read_register(r.KXG08_GYRO_XOUT_L, 1)[0]      # gyro releases drdy latch
    while not sensor.read_drdy(intpin, channel): pass               # wait until next sample is ready
    while sensor.read_drdy(intpin, channel):                        # wait until sample ready and release drdy bit
        if channel == CH_ACC:
            data = sensor.read_register(r.KXG08_ACCEL_XOUT_L, 1)[0]   # acc releases drdy latch
        else:
            data = sensor.read_register(r.KXG08_GYRO_XOUT_L, 1)[0]  # gyro releases drdy latch
    while not sensor.read_drdy(intpin, channel):                    # finally wait beginning of drdy not ready (transition edge)
        count += 1
    assert count > 0,'Data overflow. Maybe ODR is too high for host adapter'
