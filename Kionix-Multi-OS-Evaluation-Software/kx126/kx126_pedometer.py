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
"""
KX126 pedometer
"""
## Example application for basic pedometer step counting
###
## Pedometer uses interrupts int1 for the step event and int2 for the watermark event
###
## Pedometer outputs
##
## ins1, STPOVI = step overflow event
## ins1, STPWMI = step watermark event
## ins2, STPINCI = step counter increment event

_CODE_FORMAT_VERSION = 2.0
 
import time
from imports import *
from lib.data_stream import stream_config, timenow_str, start_time_str, end_time_str
from lib.proto import ProtocolException

class Pedometer_parameters_odr_50:
### Pedometer algorithm settings, configuration ODR_50, ODR = 50 Hz.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_8'] #b.KX126_PED_CNTL1_STP_TH_STEP_8 
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['50'] # b.KX126_PED_CNTL2_PED_ODR_50
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x10)
    M_H         =   (0x0A)
    M_L         =   (0x0B)
    T_L         =   (0x05)
    T_M         =   (0x10)
    T_P         =   (0x0A)

class Pedometer_parameters_odr_100:
### Pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_12'] #b.KX126_PED_CNTL1_STP_TH_STEP_12 # 12 steps(0x06 << 4) # ? 
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100'] # b.KX126_PED_CNTL2_PED_ODR_100 # ?(0x0C << 0) 
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x24)
    M_H         =   (0x13)
    M_L         =   (0x0B)
    T_L         =   (0x08)
    T_M         =   (0x19)
    T_P         =   (0x1C)

class kx126_pedometer_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self, sensor)

        # define the data stream
        ped_gpio_pin  = 1 # index number
        self.define_request_message(\
                                    fmt = "<BBBBBBB",
                                    hdr = "ch!ins1!ins2!ins3!stat!N/A!rel",
                                    reg = r.KX126_INS1,
                                    pin_index=ped_gpio_pin)

def set_pedometer_parameters(sensor, cfg):
    ## PED_CNTL1
    ##      STP_TH; first accepted step count level = default 8 (0x4)
    ##      MAG_SCALE; signal scaling = default 6
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, cfg.STP_TH, m.KX126_PED_CNTL1_STP_TH_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, cfg.MAG_SCALE, m.KX126_PED_CNTL1_MAG_SCALE_MASK)

    ## PED_CNTL2
    ##      HPS; Scaling factor for the output from the high-pass filter = default 3
    ##      LP_LEN; The length of the low-pass filter = default 100Hz (0x0c)
    ## default 03 changed due 8g mode in asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, cfg.HPS, m.KX126_PED_CNTL2_HPS_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, cfg.LP_LEN, m.KX126_PED_CNTL2_PED_ODR_MASK)
        
    ## PED_CNTL3
    ##      FCB; Scaling factors inside the high-pass filter = default 0x01, changed due to the 8g mode in the asic
    ##      FCA; Default 0x0E, changed due to the 8g mode in the asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, cfg.FCB, m.KX126_PED_CNTL3_FCB_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, cfg.FCA, m.KX126_PED_CNTL3_FCA_MASK)
 
    ## PED_CNTL4
    ##      B_CNT; Samples below the zero threshold before setting = default 0x1
    ##      A_H; Maximum area of the peak (maximum impact from the floor) = default 0x0F
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, cfg.B_CNT, m.KX126_PED_CNTL4_B_CNT_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, cfg.A_H, m.KX126_PED_CNTL4_A_H_MASK)
    
    ## PED_CNTL5
    ##      A_L; Minimum area of the peak (minimum impact from the floor) = default 0x3C
    sensor.write_register(r.KX126_PED_CNTL5, cfg.A_L)
            
    ## PED_CNTL6
    ##      M_H; maximum time interval for the peak = default 0x14
    sensor.write_register(r.KX126_PED_CNTL6, cfg.M_H)
    
    ## PED_CNTL7
    ##      M_L         - minimum time interval for the peak = default 0x06
    sensor.write_register(r.KX126_PED_CNTL7, cfg.M_L)
    
    ## PED_CNTL8
    ##      T_L         - time window for noise and delay time = default 0x05
    sensor.write_register(r.KX126_PED_CNTL8, cfg.T_L)
        
    ## PED_CNTL9
    ##      T_M         - time interval to prevent overflowing = default 0x16
    sensor.write_register(r.KX126_PED_CNTL9, cfg.T_M)
    
    ## PED_CNTL10
    ##      T_P         - minimum time interval for a single stride = default 0x13
    sensor.write_register(r.KX126_PED_CNTL10, cfg.T_P)

## enable measurement and pedometer logger
def kx126_enable_pedometer_logger(sensor, odr = 100, avg = 128):
    logger.info('Pedometer step counting init start')

    # turn sensor off
    sensor.set_power_off()         # this sensor request PC=0 to PC=1 before valid settings
  
    # set watermark interrupt level
    #sensor.set_pedometer_watermark(0x14)
    
    # "disable" watermark
    sensor.set_pedometer_watermark(0xffff)

    assert odr in [50,100]
    
    if odr == 50:
        # run pedometer with 50Hz ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_50, m.KX126_PED_CNTL2_PED_ODR_MASK)
    else: # run pedometer with 100Hz ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_100, m.KX126_PED_CNTL2_PED_ODR_MASK)

    # TODO use enum 
    if  avg == 0: # no averaging
        sensor.set_average(b.KX126_LP_CNTL_AVC_NO_AVG)
    elif avg == 2: # set averaging to 2 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_2_SAMPLE_AVG)
    elif avg == 4: # set averaging to 4 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_4_SAMPLE_AVG)
    elif avg == 8: # set averaging to 8 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_8_SAMPLE_AVG)
    elif avg == 16: # set averaging to 16 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_16_SAMPLE_AVG)
    elif avg == 32: # set averaging to 32 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_32_SAMPLE_AVG)
    elif avg == 64: # set averaging to 64 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_64_SAMPLE_AVG)
    elif avg == 128: # set averaging to 128 samples - high performance mode
        sensor.set_average(b.KX126_LP_CNTL_AVC_128_SAMPLE_AVG)
    else: sensor.set_average(b.KX126_LP_CNTL_AVC_128_SAMPLE_AVG) # Default number for averaging

    # configure interrupts  
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPOVI2) # overflow interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPWMI2) # watermark interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPINCI2) # step counter increment interrupt to INT2
    
    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2 ) # enable INT2
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEA2 ) # active low 
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2 ) # latched interrupt
    
    sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_PDE ) # enable pedometer
    
    logger.info('Pedometer step counting initialized')
    # TODO power on sensor here, not in app_main()
    #sensor.set_power_on()                             # power on the sensor

def read_with_polling(sensor, loop):
    count = 0
   
    try:
        while count < loop or loop is None:
            ins1 = sensor.read_register(r.KX126_INS1)[0]
            ins2 = sensor.read_register(r.KX126_INS2)[0]
            now = timing.time_elapsed()
            
            # pedometer interrupts
            if ins1 & b.KX126_INS1_STPWMI:
                logger.info('KX126_INS1_STPWMI')
                print 'WMI steps',sensor.read_step_count()

            if ins2 & b.KX126_INS2_STPINCI:
                logger.info('KX126_INS2_STPINCI')
                print '%f%s%d%s%d%s%d' % (now,DELIMITER,10, DELIMITER, ins1, DELIMITER, ins2)

            if ins1 & b.KX126_INS1_STPOVI:
                logger.debug('KX126_INS1_STPOVI')

            # other interrupts
            if ins2 & b.KX126_INS2_WMI:
                logger.debug('KX126_INS2_WMI')

            if ins2 & b.KX126_INS2_BFI:
                logger.debug('KX126_INS2_BFI')

            if ins2 & b.KX126_INS2_FFS:
                logger.debug('KX126_INS2_FFS')

            if ins2 ^ b.KX126_INS2_DRDY != 0:
                #print '%f%s%d%s%d%s%d' % (now,DELIMITER,10, DELIMITER, ins1, DELIMITER, ins2)
                sensor.release_interrupts()
                count += 1
                    
    except(KeyboardInterrupt):
        pass
    
    finally:
        logger.info('bye')

def read_with_stream(sensor, loop=None):
    stream = kx126_pedometer_data_stream(sensor)
    stream.read_data_stream(loop=loop,
                            max_timeout_count = None)
    
    return stream

def enable_data_logging(sensor, odr = 100, cfg = Pedometer_parameters_odr_100, avg = 128):
    
    kx126_enable_pedometer_logger(sensor, odr, avg)

    set_pedometer_parameters(sensor, cfg)
    sensor.set_power_on()

def app_main(odr = 100):
    # A default number of AVG samples for the pedometer engine
    avg = 16
    # Select configuration related to the ODR
    #conf = Pedometer_parameters_odr_50  # The best configuration with 50 Hz ODR.
    conf = Pedometer_parameters_odr_100  # The best configuration with 100 Hz ODR.
    # conf = xxx  # Some other configuration.

    sensor = kx126_driver()
    bus = open_bus_or_exit(sensor)

    enable_data_logging(sensor, odr, cfg = conf, avg = avg)
    
    logger.info('kx126_pedometer; '+'ODR: ' + str(odr)+' Hz, '+'configuration: '+str(conf)+', avg: '+str(avg)+' samples')
    timing.reset()
    args = get_datalogger_args()   
    if args.stream_mode:
        logger.info('Read with stream')
        print '\n'
        read_with_stream(sensor, args.loop)
    else:
        logger.info('Read with polling')
        print "\n"
        read_with_polling(sensor, args.loop)

    print 'Steps counted:', sensor.read_step_count()

    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()
