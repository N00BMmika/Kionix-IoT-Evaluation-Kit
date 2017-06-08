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
## basic logger for KXG03
###
## polling or stream
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class kxg03_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)

        # TODO make this dictionary
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            pin_index = 0
        else:
            pin_index = 1

        self.define_request_message(sensor,
                                    fmt = "<Bhhhhhhh",
                                    hdr = "ch!temperature!gx!gy!gz!ax!ay!az",
                                    reg = r.KXG03_TEMP_OUT_L,
                                    pin_index=pin_index)
    
def enable_data_logging(sensor, odr = 25):
    logger.debug('enable_data_logging start')
    sensor.set_power_off()  # this sensor request PC=0 to PC=1 before valid settings

    ## set odrs
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.KXG03_ACCEL_ODR_WAKE_ODRA_W[odr],
                   e.KXG03_ACCEL_ODR_SLEEP_ODRA_S[odr], CH_ACC)     # wake and sleep
    sensor.set_odr(e.KXG03_GYRO_ODR_WAKE_ODRG_W[odr], 
                   e.KXG03_GYRO_ODR_SLEEP_ODRG_S[odr], \
                   CH_GYRO)                                         # wake and sleep

    ## select ranges
    sensor.set_range(b.KXG03_ACCEL_CTL_ACC_FS_W_2G,
                     b.KXG03_ACCEL_CTL_ACC_FS_S_2G, \
                     CH_ACC)                                        # wake and sleep
    
    sensor.set_range(b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_2048,
                     b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_2048, \
                     CH_GYRO)                                       # wake and sleep

    ## Low power mode selections; can be also mixed for wake and sleep modes
    LOW_POWER_MODE = False
    if LOW_POWER_MODE == True:
        power_modes(sensor, LPMODE, WAKE)
        power_modes(sensor, LPMODE, SLEEP)
        sensor.set_average(b.KXG03_ACCEL_ODR_WAKE_NAVG_W_16_SAMPLE_AVG,
                           b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_2_SAMPLE_AVG, \
                           CH_ACC)                                  # only in low power mode, for wake and sleep modes     
    else:
        power_modes(sensor, FULL_RES, WAKE)
        power_modes(sensor, FULL_RES, SLEEP)
        
    ## averaging for acc and BW for gyro
    sensor.set_BW(b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_10,
                  b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_10, CH_GYRO)     # wake and sleep
    ## interrupts
    sensor.set_bit_pattern(r.KXG03_INT_PIN1_SEL, 0x00, 0xff)        # routing int1 none
    sensor.set_bit_pattern(r.KXG03_INT_MASK1, 0x00, 0xff)           # mask none
    sensor.set_bit_pattern(r.KXG03_INT_PIN2_SEL, 0x00, 0xff)        # routing int2 none
    ## data ready settings
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        #sensor.enable_drdy(1, CH_ACC)                               # acc data ready to int1
        sensor.enable_drdy(1, CH_GYRO)                            # gyro data ready to int1
        sensor.set_bit(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN1)
    elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
        #sensor.enable_drdy(2, CH_ACC)                               # acc data ready to int2
        sensor.enable_drdy(2, CH_GYRO)                            # gyro data ready to int2
        sensor.set_bit(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN2)
    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        ## drdy must be enabled also when polling
        #sensor.enable_drdy(1, CH_ACC)
        sensor.enable_drdy(1, CH_GYRO)
    ## interrupt signal parameters
    sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                           b.KXG03_INT_PIN_CTL_IEL1_LATCHED, 
                           m.KXG03_INT_PIN_CTL_IEL1_MASK)
    
    sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                           b.KXG03_INT_PIN_CTL_IEL2_LATCHED, 
                           m.KXG03_INT_PIN_CTL_IEL2_MASK)
    
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                               b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_HIGH, 
                               m.KXG03_INT_PIN_CTL_IEA1_MASK)        
    else:
        sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                               b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_LOW, 
                               m.KXG03_INT_PIN_CTL_IEA1_MASK)
        
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                               b.KXG03_INT_PIN_CTL_IEA2_ACTIVE_HIGH, 
                               m.KXG03_INT_PIN_CTL_IEA2_MASK) 
    else:
        sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                               b.KXG03_INT_PIN_CTL_IEA2_ACTIVE_LOW, 
                               m.KXG03_INT_PIN_CTL_IEA2_MASK)  
        
    ## change mode (for start)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)

    ## power sensor(s)
    sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)                # acc + gyro + temp ON
    
    #sensor.register_dump(); sys.exit()

    logger.debug('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header    
    print DELIMITER.join(['#timestamp','10','temperature','gx','gy','gz','ax','ay','az'])
    
    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            temp, gx, gy, gz, ax, ay, az = sensor.read_data(CH_GYRO | CH_ACC | CH_TEMP)
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [temp, gx, gy, gz, ax, ay, az])

    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    stream = kxg03_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream
 
if __name__ == '__main__':
    sensor = kxg03_driver()
    bus = open_bus_or_exit(sensor)
    
    enable_data_logging(sensor)

    timing.reset()
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()
