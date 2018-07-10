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
KX022 data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *


class kx022_data_stream(stream_config):

    def __init__(self, sensor, pin_index=None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        assert pin_index in [0, 1]

        # Default way to define request message
        self.define_request_message(
            fmt="<Bhhh",
            hdr="ch!ax!ay!az",
            reg=r.KX022_XOUT_L,
            pin_index=pin_index)

        # Advanced way to define request message
# self.define_request_message(\
##                                    fmt = "<Bhhh"+ext.fmt_packet_count_8,
##                                    hdr = "ch!ax!ay!az"+ext.hdr_packet_count_8,
##                                    reg = [sensor.address(), r.KX022_XOUT_L, 6] + ext.reg_packet_count_8,
# pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=25,
                        max_range='2G',
                        lp_mode=False,
                        filter = 'ODR_9',
                        power_off_on=True       # set to False if this function is part of other configuration
                        ):
    logger.info('enable_data_logging start')

    #
    # parameter validation
    #
    
    if sensor.WHOAMI in sensor._WAIS122:
        valid_odrs = e122.KX122_ODCNTL_OSA.keys()
    else:
        valid_odrs = e.KX022_ODCNTL_OSA.keys()

    assert convert_to_enumkey(odr) in valid_odrs,\
    'Invalid odr value "{}". Valid values are {}'.format(
    odr,valid_odrs)
    
    assert max_range in e.KX022_CNTL1_GSEL.keys(), \
    'Invalid max_range value "{}". Valid values are {}'.format(
    max_range, e.KX022_CNTL1_GSEL.keys())

    assert lp_mode in e.KX022_LP_CNTL_AVC.keys() + [False], \
    'Invalid lp_mode value "{}". Valid values are: False or {}'.format(
    lp_mode,e.KX022_LP_CNTL_AVC.keys())
        
    assert filter in e.KX022_ODCNTL_LPRO.keys() + ['BYPASS'], \
    'Invalid filter value "{}". Valid values are: BYPASS or {}'.format(
    filter,e.KX022_ODCNTL_LPRO.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # odr setting for data logging
    if sensor.WHOAMI in sensor._WAIS122:
        sensor.set_odr(e122.KX122_ODCNTL_OSA[convert_to_enumkey(odr)])
    else:
        sensor.set_odr(e.KX022_ODCNTL_OSA[convert_to_enumkey(odr)])

    # select g-range
    sensor.set_range(e.KX022_CNTL1_GSEL[max_range])

    # resolution / power mode selection

    if lp_mode is not False:
        # enable low current mode
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)
        # define averaging value
        sensor.set_average(e.KX022_LP_CNTL_AVC[lp_mode])
    else:
        # full resolution
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)

    # set bandwitdh
    if filter != 'BYPASS':
        sensor.set_BW(e.KX022_ODCNTL_LPRO[filter], 0, CH_ACC)
        sensor.enable_iir()
    else:
        sensor.disable_iir()
    #
    # interrupt pin routings and settings
    #

    # select dataready routing for sensor = int1, int2 or register polling

    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        # latched interrupt int1
        sensor.enable_drdy(intpin=1)
        sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)
        sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEN1)     # interrupt 1 set

        if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
            sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_HIGH)
        else:
            sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_LOW)

    elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
        # latched interrupt int2
        sensor.enable_drdy(intpin=2)
        sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)
        sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEN2)     # interrupt 2 set

        if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
            sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_HIGH)
        else:
            sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_LOW)

    else:  # evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when register polling
        sensor.enable_drdy(intpin=1)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    timing.reset()
    print (start_time_str())

    # print log header. 10 is channel number
    print (DELIMITER.join(['#timestamp', '10', 'ax', 'ay', 'az']))

    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            ax, ay, az = sensor.read_data()
            print ('{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) +
                   DELIMITER.join('{:d}'.format(t) for t in [ax, ay, az]))

    except (KeyboardInterrupt):
        print (end_time_str())


def read_with_stream(sensor, loop):
    stream = kx022_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream



def app_main(odr=25):
    sensor = kx022_driver()
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
