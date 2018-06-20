# The MIT License (MIT)
#
# Copyright (c) 2016 Rohm Semiconductor
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
BH1749 data logger application
"""
from imports import *
_CODE_FORMAT_VERSION = 2.0


class Bh1749DataStream(stream_config):

    def __init__(self, sensor, pin_index=None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index = 0

        assert pin_index in [0], 'Only one int in sensor'

        self.define_request_message(
            fmt="<BHHHHHB",
            hdr="ch!red!green!blue!ir!green2",
            reg=[sensor.address(), r.BH1749_RED_DATA_LSBS, 6,
                 sensor.address(), r.BH1749_IR_DATA_LSBS, 4,
                 sensor.address(), r.BH1749_INTERRUPT, 1], #ACK interrupt
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=28.6,
                        rgb_gain='1X',
                        ir_gain='1X'):

    logger.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert evkit_config.get('generic', 'drdy_operation') in \
         ['ADAPTER_GPIO1_INT', 'DRDY_REG_POLL', 'INTERVAL_READ'],\
        'Only one int in sensor, check drdy_operation setting.'
    assert rgb_gain in e.BH1749_MODE_CONTROL1_RGB_GAIN, \
        'Invalid value for RGBC gain. Valid values are %s' % \
        e.BH1749_MODE_CONTROL1_RGB_GAIN.keys()

    assert ir_gain in e.BH1749_MODE_CONTROL1_IR_GAIN, \
        'Invalid value for IR gain. Valid values are %s' % \
        e.BH1749_MODE_CONTROL1_IR_GAIN.keys()


    #
    # interrupt pin routings and settings
    #
    sensor.set_interrupt_persistence(
        b.BH1749_PERSISTENCE_MODE_STATUS_ACTIVE_AFTER_MEASUREMENT)

    # select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_int_pin()     # interrupt 1 set
    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        sensor.disable_int_pin()

    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        logger.warning(
            'Active high interrupt not supported. Using active low interrupt.')

    sensor.start_measurement(
        e.BH1749_MODE_CONTROL1_ODR[convert_to_enumkey(odr)],
        e.BH1749_MODE_CONTROL1_RGB_GAIN[rgb_gain],
        e.BH1749_MODE_CONTROL1_IR_GAIN[ir_gain])

    logger.debug('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header
    print DELIMITER.join(['#timestamp', '10', 'red', 'green', 'blue', 'ir', 'green2'])

    try:
        while count < loop or loop is None:
            count += 1

            sensor.drdy_function()
            sensor.clear_interrupt()
            now = timing.time_elapsed()
            red, green, blue, ir, green2 = sensor.read_data()

            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + \
                  DELIMITER.join('{:d}'.format(t) for t in [red, green, blue, ir, green2])

    except KeyboardInterrupt:
        print end_time_str()

    finally:
        sensor.clear_interrupt()

def read_with_stream(sensor, loop):
    stream = Bh1749DataStream(sensor)
    stream.read_data_stream(loop)
    return stream


def logger_main(odr=28.6):
    sensor = bh1749_driver()

    bus = open_bus_or_exit(sensor)

    enable_data_logging(sensor, odr=odr)

    #small delay for INTERVAL_READ mode
    time.sleep(0.2)

    timing.reset()
    args = get_datalogger_args()
    if args.stream_mode:
        if stream_config_check() is True:
            read_with_stream(sensor, args.loop)
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, args.loop)

    sensor.soft_reset()
    bus.close()


if __name__ == '__main__':
    logger_main()
