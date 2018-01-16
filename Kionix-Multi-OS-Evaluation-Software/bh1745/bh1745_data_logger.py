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
BH1745 RGBC sensor data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *


class bh1745_data_stream(stream_config):
    def __init__(self, sensor, pin_index=None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index = 0

        assert pin_index in [0], 'Only one int in sensor'

        self.define_request_message(
            fmt="<BHHHHB",
            hdr="ch!red!green!blue!clear!int",
            reg=[sensor.address(), r.BH1745_RED_DATA_LSBS, 8, sensor.address(), r.BH1745_INTERRUPT, 1],
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=6.25,
                        gain='1X',
                        power_off_on=True       # set to False if this function is part of other configuration
                        ):
    logger.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT', 'DRDY_REG_POLL', 'INTERVAL_READ'],\
        'Only one int in sensor, check drdy_operation setting.'
    assert gain in e.BH1745_MODE_CONTROL2_ADC_GAIN, \
        'Invalid value for gain. Valid values are %s' % \
        e.BH1745_MODE_CONTROL2_ADC_GAIN.keys()

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # select ODR
    sensor.set_measurement_time(e.BH1745_MODE_CONTROL1_ODR[convert_to_enumkey(odr)])

    # Select adc gain
    sensor.set_adc_gain(e.BH1745_MODE_CONTROL2_ADC_GAIN[gain])

    #
    # interrupt pin routings and settings
    #

    # interrupts settings
    sensor.write_interrupt_tresholds(1, 0)      # always interrupt, kind of DRDY mode
    sensor.set_interrupt_persistence(b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_TOGGLE_AFTER_MEASUREMENT)

    # TODO use enums
    sensor.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_RED)
    # sensor.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_GREEN)
    # sensor.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_BLUE)
    # sensor.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_CLEAR)
    
    sensor.enable_interrupt_latch()

    # select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_int_pin()     # interrupt 1 set
    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        sensor.disable_int_pin()

    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    if power_off_on:
        sensor.set_power_on()

        # sensor.register_dump()#;sys.exit()
    
    logger.debug('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header
    print DELIMITER.join(['#timestamp', '10', 'red', 'green', 'blue', 'clear'])
    
    try:
        while count < loop or loop is None:
            count += 1
            
            sensor.drdy_function()
            sensor.clear_interrupt()
            now = timing.time_elapsed()
            r, g, b, c = sensor.read_data()
            
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + \
                  DELIMITER.join('{:d}'.format(t) for t in [r, g, b, c])
 
    except KeyboardInterrupt:
        print end_time_str()

    finally:
        sensor.clear_interrupt()


def read_with_stream(sensor, loop):
    stream = bh1745_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream


def logger_main(odr=6.25):
    sensor = bh1745_driver()
    bus = open_bus_or_exit(sensor)
    
    enable_data_logging(sensor, odr=odr)

    timing.reset()
    if args.stream_mode:
        if stream_config_check() is True:            
            read_with_stream(sensor, args.loop)
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()


if __name__ == '__main__':
    logger_main()
