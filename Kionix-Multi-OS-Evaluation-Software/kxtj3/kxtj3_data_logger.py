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
KXTJ3 data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *


class kxtj3_data_stream(stream_config):

    def __init__(self, sensor, pin_index = None):
        stream_config.__init__(self, sensor)
        
        if pin_index is None:
            pin_index=0

        assert pin_index in [0], 'Sensor can only be connected to adapter logical int pin 0'
            
        # Default way to define request message
        self.define_request_message(
            fmt="<BhhhB",
            hdr="ch!ax!ay!az!rel",
            reg=[sensor.address(), r.KXTJ3_XOUT_L, 6,
                 sensor.address(), r.KXTJ3_INT_REL, 1],
            pin_index=pin_index)



def enable_data_logging(sensor,
                        odr=25,
                        max_range='2G',
                        lp_mode=False,
                        power_off_on=True       # set to False if this function is part of other configuration
                        ):
    logger.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert max_range in e.KXTJ3_CTRL_REG1_GSEL.keys(), \
    'Invalid max_range value "{}". Valid values are {}'.format(
    max_range, e.KXTJ3_CTRL_REG1_GSEL.keys())
    
    assert lp_mode in [True, False],\
    'Invalid lp_mode value "{}". Valid values are {}'.format(
    lp_mode,[True,False])
    
    assert convert_to_enumkey(odr) in e.KXTJ3_DATA_CTRL_REG_OSA.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    odr, e.KXTJ3_DATA_CTRL_REG_OSA.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # odr setting for data logging
    sensor.set_odr(e.KXTJ3_DATA_CTRL_REG_OSA[convert_to_enumkey(odr)])

    # select g-range
    sensor.set_range(e.KXTJ3_CTRL_REG1_GSEL[max_range])

    # resolution / power mode selection

    if lp_mode is True:
        # enable low current mode
        sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)
    else:
        # full resolution
        sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)
    #
    # interrupt pin routings and settings
    #

    # select dataready routing for sensor = int1 or register polling

    # interrupts settings
    # select dataready routing for sensor = int1 or register polling
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy()
        # enable interrrupt pin
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)
    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy()                # drdy must be enabled also when register polling
    # interrupt signal parameters
    sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1,
                     b.KXTJ3_INT_CTRL_REG1_IEL)  # latched interrupt
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1,
                       b.KXTJ3_INT_CTRL_REG1_IEA)  # active high
    else:
        sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1,
                         b.KXTJ3_INT_CTRL_REG1_IEA)  # active low

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
            # need to release explicitely if monitoring drdy interrupt line
            sensor.release_interrupts()

    except (KeyboardInterrupt):
        print (end_time_str())


def read_with_stream(sensor, loop):
    stream = kxtj3_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=25):
    sensor = kxtj3_driver()
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
