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
KXG03 data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *

class kxg03_data_stream(stream_config):

    def __init__(self, sensor, pin_index=None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        assert pin_index in [0, 1]


        self.define_request_message(\
                                    fmt = "<Bhhhhhhh",
                                    hdr = "ch!temperature!gx!gy!gz!ax!ay!az",
                                    reg = r.KXG03_TEMP_OUT_L,
                                    pin_index=pin_index)
    
def enable_data_logging(sensor,
                        odr = 25,
                        max_range_acc='2G',
                        lp_mode=False,
                        power_off_on=True,      # set to False if this function is part of other configuration
                        int_number=None):
    logger.info('enable_data_logging start')

    #
    # parameter validation
    #
    assert int_number in [1,2,None]
    
    assert convert_to_enumkey(odr) in e.KXG03_ACCEL_ODR_WAKE_ODRA_W,\
    'Invalid odr value "{}". Support values are {}'.format(
    odr,e.KXG03_ACCEL_ODR_WAKE_ODRA_W.keys())
    
    assert convert_to_enumkey(odr) in e.KXG03_GYRO_ODR_WAKE_ODRG_W,\
    'Invalid odr value "{}". Support values are {}'.format(
    odr,e.KXG03_GYRO_ODR_WAKE_ODRG_W.keys())
    
    assert lp_mode in [True, False],\
    'Invalid lp_mode value "{}". Valid values are True and False'.format(
    lp_mode)
    
    assert max_range_acc in e.KXG03_ACCEL_CTL_ACC_FS_W,\
    'Invalid max_range_acc value "{}". Support values are {}'.format(
    max_range_acc,e.KXG03_ACCEL_CTL_ACC_FS_W.keys())
    
    assert max_range_acc in e.KXG03_ACCEL_CTL_ACC_FS_S,\
    'Invalid max_range_acc value "{}". Support values are {}'.format(
    max_range_acc,e.KXG03_ACCEL_CTL_ACC_FS_S.keys())
    
    #Set sensor to stand-by mode to enable setup change
    if power_off_on:
        sensor.set_power_off()  # this sensor request PC=0 to PC=1 before valid settings

    #
    # Configure sensor
    #

    # odr setting for data logging
    odr = convert_to_enumkey(odr)

    sensor.set_odr(e.KXG03_ACCEL_ODR_WAKE_ODRA_W[convert_to_enumkey(odr)],
                   e.KXG03_ACCEL_ODR_SLEEP_ODRA_S[convert_to_enumkey(odr)], CH_ACC)     # wake and sleep
    sensor.set_odr(e.KXG03_GYRO_ODR_WAKE_ODRG_W[convert_to_enumkey(odr)], 
                   e.KXG03_GYRO_ODR_SLEEP_ODRG_S[convert_to_enumkey(odr)], \
                   CH_GYRO)                                         # wake and sleep

    ## select ranges
    sensor.set_range(e.KXG03_ACCEL_CTL_ACC_FS_W[max_range_acc],
                     e.KXG03_ACCEL_CTL_ACC_FS_S[max_range_acc], \
                     CH_ACC)                                        # wake and sleep
    
    sensor.set_range(b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_2048,
                     b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_2048, \
                     CH_GYRO)                                       # wake and sleep

    ## Low power mode selections; can be also mixed for wake and sleep modes
    LOW_POWER_MODE = lp_mode
    if LOW_POWER_MODE == True:
        power_modes(sensor, LPMODE, WAKE)
        power_modes(sensor, LPMODE, SLEEP)
        # TODO add different averaging modes
        sensor.set_average(b.KXG03_ACCEL_ODR_WAKE_NAVG_W_16_SAMPLE_AVG,
                           b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_2_SAMPLE_AVG, \
                           CH_ACC)                                  # only in low power mode, for wake and sleep modes     
    else:
        power_modes(sensor, FULL_RES, WAKE)
        power_modes(sensor, FULL_RES, SLEEP)
        
    ## averaging for acc and BW for gyro
    sensor.set_BW(b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_10,
                  b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_10, CH_GYRO)     # wake and sleep
    #
    # interrupt pin routings and settings
    #

    sensor.write_register(r.KXG03_INT_PIN1_SEL, 0x00)        # routing int1 none
    sensor.write_register(r.KXG03_INT_PIN2_SEL, 0xff)        # routing int2 none
    sensor.write_register(r.KXG03_INT_MASK1,    0x00)        # mask none

    ## data ready settings

    if int_number == None:
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            int_number = 1
        elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
            int_number = 2
        else:
            int_number = -1 # DRDY_REG_POLL
            
    if int_number == 1:
        #sensor.enable_drdy(1, CH_ACC)                               # acc data ready to int1
        sensor.enable_drdy(1, CH_GYRO)                            # gyro data ready to int1
        sensor.set_bit(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN1)   # enable interrupt pin 1

        if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
            sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_HIGH)
        else:
            sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_LOW)
    elif int_number == 2:
        #sensor.enable_drdy(2, CH_ACC)                               # acc data ready to int2
        sensor.enable_drdy(2, CH_GYRO)                            # gyro data ready to int2
        sensor.set_bit(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN2)   # enable interrupt pin 2

        if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
            sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_HIGH)
        else:
            sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_LOW)

    else:  # evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when polling
        #sensor.enable_drdy(1, CH_ACC)
        sensor.enable_drdy(1, CH_GYRO)

    ## interrupt signal parameters

    sensor.set_bit_pattern(r.KXG03_INT_PIN_CTL, 
                           b.KXG03_INT_PIN_CTL_IEL1_LATCHED | b.KXG03_INT_PIN_CTL_IEL2_LATCHED,  
                           m.KXG03_INT_PIN_CTL_IEL1_MASK | m.KXG03_INT_PIN_CTL_IEL2_MASK)
    ## change mode (for start)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)

    # sensor.register_dump()#;sys.exit()

    logger.debug('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    timing.reset()
    print (start_time_str())

    # print log header. 10 is channel number
    print (DELIMITER.join(['#timestamp','10','temperature','gx','gy','gz','ax','ay','az']))
    
    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            temp, gx, gy, gz, ax, ay, az = sensor.read_data(CH_GYRO | CH_ACC | CH_TEMP)
            print ('{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [temp, gx, gy, gz, ax, ay, az]))

    except (KeyboardInterrupt):
        print (end_time_str())


def read_with_stream(sensor, loop):
    stream = kxg03_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=25):
    sensor = kxg03_driver()
    bus = open_bus_or_exit(sensor)
    enable_data_logging(sensor, odr=odr)
    args = get_datalogger_args() 
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()


if __name__ == '__main__':
    app_main()
