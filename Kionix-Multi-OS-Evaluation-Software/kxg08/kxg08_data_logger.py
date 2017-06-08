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
## data logger application for KXG07 and KXG08
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class kxg08_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)

        # TODO make this dictionary
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            pin_index = 0
        else:
            pin_index = 1

        self.define_request_message(sensor,
                                    fmt = "<BhhhhhhB",
                                    hdr = "ch!gx!gy!gz!ax!ay!az!ind",
                                    reg = [sensor.address(),r.KXG08_GYRO_XOUT_L,12,
                                           0xff,0x00,0x00],
                                    pin_index=pin_index)
def enable_data_logging(sensor, odr = 25, acc_fs = '2g', gyro_fs = 1024):
    logger.debug('enable_data_logging start')    
    ## set odrs
    odr = convert_to_enumkey(odr)
    gyro_fs = convert_to_enumkey(gyro_fs)

    assert gyro_fs in ['64','128','256','512','1024','2048']
    assert acc_fs in ['2g','4g','8g','16g']
    
    sensor.set_odr(e.KXG08_ACCEL_ODR_ODRA[odr], None, CH_ACC)      # acc odr
    sensor.set_odr(e.KXG08_GYRO_ODR_ODRG[odr],  None, CH_GYRO)     # gyro odr

    ## select g range
    
    #sensor.set_range(b.KXG08_ACCEL_CTL_ACC_FS_2G,  None, CH_ACC)    # acc range
    sensor.set_range(e.KXG08_ACCEL_CTL_ACC_FS[acc_fs], None, CH_ACC)    # acc range
    
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_64,   None, CH_GYRO)  # gyro range
    sensor.set_range(e.KXG08_GYRO_CTL_GYRO_FS[gyro_fs], None, CH_GYRO)  # gyro range]
    
    LOW_POWER_MODE = False
    if LOW_POWER_MODE == True:
        power_modes(sensor, LPMODE, None, CH_ACC)                  # power mode for acc 
        power_modes(sensor, LPMODE, None, CH_GYRO)                 # power mode for gyro            
        ## averaging 
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG, CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_64_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_32_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_16_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_8_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_4_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_2_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_NO_AVG,         CH_ACC)      # acc low power mode
        ## averaging for gyro only with version 2080
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG, CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_64_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_32_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_16_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_8_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_4_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_2_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_NO_AVG,         CH_GYRO)      # gyro low power mode
    else:
        power_modes(sensor, FULL_RES, None, CH_ACC)                 # power mode for acc        
        power_modes(sensor, FULL_RES, None, CH_GYRO)                # power mode for gyro
 
    ## bandwidth
    #sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, CH_ACC)       # bandwidth acc      
    sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_8, CH_ACC)       # bandwidth acc 
    #sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, CH_GYRO)      # bandwidth gyro
    sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_8, CH_GYRO)      # bandwidth gyro

    ## interrupts
    sensor.set_bit_pattern(r.KXG08_INT_PIN_SEL1, 0x00, 0xff)    # routings off
    sensor.set_bit_pattern(r.KXG08_INT_PIN_SEL2, 0x00, 0xff)    # 
    sensor.set_bit_pattern(r.KXG08_INT_PIN_SEL3, 0x00, 0xff)    # 
    sensor.set_bit_pattern(r.KXG08_INT_MASK1, 0x00, 0xff)       # masks all ints out    
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(1, CH_ACC)                                   # acc data ready to int1
        #sensor.enable_drdy(1, CH_GYRO)                                 # gyro data ready to int1
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':
        sensor.enable_drdy(2, CH_ACC)                                   # acc data ready to int2
        #sensor.enable_drdy(2, CH_GYRO)                                 # gyro data ready to int2
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when polling
        sensor.enable_drdy(1, CH_ACC)
    ## interrupt signal parameters
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        IEA1 = b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH
    else:
        IEA1 = b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW      
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        IEA2 = b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH
    else:
        IEA2 = b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW
    sensor.set_bit_pattern(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEN2 | \
                                                IEA2 | \
                                                b.KXG08_INT_PIN_CTL_IEL2_LATCHED | \
                                                b.KXG08_INT_PIN_CTL_IEN1 | \
                                                IEA1 | \
                                                b.KXG08_INT_PIN_CTL_IEL1_LATCHED, \
                                                0xff)                       # both int pins active

    ## change mode (manual)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)
    
    ## power sensor(s)
    #sensor.set_power_on(CH_ACC )                                   # acc ON
    #sensor.set_power_on(CH_ACC | CH_GYRO )                         # acc + gyro ON
    sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP )                # acc + gyro + temp ON

    #sensor.register_dump()#;sys.exit()

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
    stream = kxg08_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream
    
if __name__ == '__main__':
    sensor = kxg08_driver()
    bus = open_bus_or_exit(sensor)
    
    enable_data_logging(sensor)
    
    timing.reset()
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()
