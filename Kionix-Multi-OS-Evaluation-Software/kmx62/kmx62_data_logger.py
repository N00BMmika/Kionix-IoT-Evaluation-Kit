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
KMX62 accelerometer/magnetomter sensor data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *


class kmx62_data_stream(stream_config):

    def __init__(self, sensor, pin_index=None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        assert pin_index in [0, 1]
        self.define_request_message(
            fmt="<Bhhhhhhh",
            hdr="ch!ax!ay!az!mx!my!mz!temp",
            reg=r.KMX62_ACCEL_XOUT_L,
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=25,
                        max_range_acc='2G',
                        lp_mode=False,
                        power_off_on=True,
                        int_number=None):

    logger.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert convert_to_enumkey(odr) in e.KMX62_ODCNTL_OSA.keys(),\
    'Invalid odr_OSA value "{}". Support values are {}'.format(
    odr,e.KMX62_ODCNTL_OSA.keys())
    
    assert max_range_acc in e.KMX62_CNTL2_GSEL, \
   'Invalid range value "{}". Support values are {}'.format(
    max_range_acc, e.KMX62_CNTL2_GSEL.keys())
    
    assert lp_mode in e.KMX62_CNTL2_RES.keys() + [False],\
    'Invalid lp_mode value "{}". Support values are {} and False'.format(
    lp_mode, e.KMX62_CNTL2_RES.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #
    # Select acc ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSA[convert_to_enumkey(odr)], CH_ACC)
    # Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[convert_to_enumkey(odr)], CH_MAG)
    
    # select g-range (for acc)
    sensor.set_range(e.KMX62_CNTL2_GSEL[max_range_acc])

    # power mode (accelerometer and magnetometer)
    if lp_mode not in ['MAX1','MAX2',False]:
        # Low power mode
        sensor.set_average(e.KMX62_CNTL2_RES[lp_mode], None, CH_ACC)
    else:
        # Full power mode
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2, None, CH_ACC)

    #
    # interrupt pin routings and settings
    #
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        IEA1 = b.KMX62_INC3_IEA1_HIGH
    else:
        IEA1 = b.KMX62_INC3_IEA1_LOW
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        IEA2 = b.KMX62_INC3_IEA2_HIGH
    else:
        IEA2 = b.KMX62_INC3_IEA2_LOW

    if int_number is None:
        ## KMX62: interrupt source selection activates also physical interrupt pin    
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            sensor.enable_drdy(1, CH_ACC)                       # acc data ready to int1
            #sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
        elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
            sensor.enable_drdy(2, CH_ACC)                       # acc data ready to int2
            #sensor.enable_drdy(2, CH_MAG)                       # mag data ready to int2        
        elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
            sensor.enable_drdy(1, CH_ACC)                       # acc data ready to int1
            #sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
    else:
        sensor.enable_drdy(int_number, CH_ACC)

    # interrupt signal parameters
    # TODO replace with write_register since whole byte is written
    sensor.set_bit_pattern(r.KMX62_INC3, b.KMX62_INC3_IEL1_LATCHED   |  \
                                         IEA1                        |  \
                                         b.KMX62_INC3_IED1_PUSHPULL  |  \
                                         b.KMX62_INC3_IEL2_LATCHED   |  \
                                         IEA2                        |  \
                                         b.KMX62_INC3_IED2_PUSHPULL,    \
                                         0xff)
    #
    # Turn on operating mode (disables setup)
    #

    # start measurement
    #sensor.set_power_on(CH_MAG )                       # mag ON
    #sensor.set_power_on(CH_ACC | CH_MAG )              # acc + mag ON
    if power_off_on:
        sensor.set_power_on(CH_ACC | CH_MAG | CH_TEMP)
    #sensor.register_dump()#;sys.exit()
    
    #sensor.read_data(CH_ACC | CH_MAG | CH_TEMP)     # this latches data ready interrupt register and signal
    
    #sensor.release_interrupts()                     # clear all internal function interrupts
    
    logger.info('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    timing.reset()
    print (start_time_str())

    # print log header
    print DELIMITER.join(['#timestamp', '10', 'ax', 'ay', 'az', 'mx', 'my', 'mz', 'temp'])

    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            ax, ay, az, mx, my, mz, temp = sensor.read_data(
                CH_ACC | CH_MAG | CH_TEMP)
            print '{:.7f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [ax, ay, az, mx, my, mz, temp])

    except (KeyboardInterrupt):
        print (end_time_str())


def read_with_stream(sensor, loop):
    stream = kmx62_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream

def app_main(odr=25):
    sensor = kmx62_driver()
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
