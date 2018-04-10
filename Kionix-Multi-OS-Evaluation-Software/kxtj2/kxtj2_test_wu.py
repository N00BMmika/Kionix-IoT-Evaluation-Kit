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
Wakeup demonstration
"""
# Example basic application for wakeup detection
_CODE_FORMAT_VERSION = 2.0
from imports import *


class Parameter_set_1:
    # low power, low odr
    LOW_POWER_MODE = True      # low power or full resolution mode
    odr = 0.781                # ODR for sensor
    wuf_THRESHOLD = 7        # 1 lsb = 62.5mg /2g range
    wuf_TIMER = 2        # owuf odr 25Hz
    wuf_ODR = 25


# native / rotated directions
resultResolverToString = {
    b.KXTJ2_INT_SOURCE2_XNWU: "x-",
    b.KXTJ2_INT_SOURCE2_XPWU: "x+",
    b.KXTJ2_INT_SOURCE2_YNWU: "y-",
    b.KXTJ2_INT_SOURCE2_YPWU: "y+",
    b.KXTJ2_INT_SOURCE2_ZNWU: "z-",
    b.KXTJ2_INT_SOURCE2_ZPWU: "z+"}


class kxtj2_wu_stream(stream_config):

    def __init__(self, sensor, pin_index=0):
        stream_config.__init__(self, sensor)
        assert pin_index in [0]

        self.define_request_message(
            fmt="BBBBBB",
            hdr="ch!INT_SOURCE1!INT_SOURCE2!STATUS_REG!NA!INT_REL",
            reg=r.KXTJ2_INT_SOURCE1,
            pin_index=pin_index)


def enable_wakeup(sensor,
                  direction_mask=b.KXTJ2_INT_CTRL_REG2_XNWU |      # x- direction mask
                  b.KXTJ2_INT_CTRL_REG2_XPWU |      # x+ direction mask
                  b.KXTJ2_INT_CTRL_REG2_YNWU |      # y- direction mask
                  b.KXTJ2_INT_CTRL_REG2_YPWU |      # y+ direction mask
                  b.KXTJ2_INT_CTRL_REG2_ZNWU |      # z- direction mask
                  b.KXTJ2_INT_CTRL_REG2_ZPWU,       # z+ direction mask
                  cfg=Parameter_set_1,
                  power_off_on=True       # set to False if this function is part of other configuration
                  ):

    logger.info('Wakeup event init start')

    #
    # parameter validation
    #

    assert convert_to_enumkey(cfg.odr) in e.KXTJ2_DATA_CTRL_REG_OSA.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    cfg.odr,e.KXTJ2_DATA_CTRL_REG_OSA.keys())
    
    assert cfg.LOW_POWER_MODE in [True, False],\
    'Invalid cfg.LOW_POWER_MODE value "{}". Valid values are True and False'.format(
    cfg.LOW_POWER_MODE)

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
        
    #
    #Configure Sensor
    #    

    # g-range is fixed +-8g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # low current
        sensor.reset_bit(r.KXTJ2_CTRL_REG1, b.KXTJ2_CTRL_REG1_RES)
    else:
        # full resolution
        sensor.set_bit(r.KXTJ2_CTRL_REG1, b.KXTJ2_CTRL_REG1_RES)

    # enable wakeup engine
    sensor.set_bit(r.KXTJ2_CTRL_REG1, b.KXTJ2_CTRL_REG1_WUFE)
    # stream odr (if stream odr is biggest odr, it makes effect to current
    # consumption)
    sensor.set_odr(e.KXTJ2_DATA_CTRL_REG_OSA[convert_to_enumkey(cfg.odr)])
    # Set wuf detection odr
    sensor.set_bit_pattern(r.KXTJ2_CTRL_REG2,
                           e.KXTJ2_CTRL_REG2_OWUF[convert_to_enumkey(
                               cfg.wuf_ODR)],
                           m.KXTJ2_CTRL_REG2_OWUF_MASK)

    #
    # Init wuf detection engine
    #

    # WUF direction definition
    sensor.write_register(r.KXTJ2_INT_CTRL_REG2, direction_mask)
    # WUF timer
    sensor.write_register(r.KXTJ2_WAKEUP_THRESHOLD, cfg.wuf_THRESHOLD)
    # WUF threshold
    sensor.write_register(r.KXTJ2_WAKEUP_TIMER, cfg.wuf_TIMER)

    #
    # interrupt pin routings and settings
    #

    # enable interrrupt pin
    sensor.set_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEN)

    # latched interrupt
    sensor.reset_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEL)
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ2_INT_CTRL_REG1,
                       b.KXTJ2_INT_CTRL_REG1_IEA)  # active high
    else:
        sensor.reset_bit(r.KXTJ2_INT_CTRL_REG1,
                         b.KXTJ2_INT_CTRL_REG1_IEA)  # active low

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('Wakeup event initialized.')


def wu_bits_to_str(int_source2):
    "Convert content of int_source2 register to movement directions"
    direction_list = []
    for i in range(0, 6):
        j = 0x01 << i
        if int_source2 & j > 0:
            direction_list.append(resultResolverToString[j])

    return ' '.join(direction_list)


def determine_wu_direction(data):
    channel, int_source1, int_source2, status_reg, NA, rel = data
    print ('WAKEUP DETECTION streming mode:' + wu_bits_to_str(int_source2))
    return True  # Continue reading


def read_with_stream(sensor, loop):
    # Note pin_index = 0
    stream = kxtj2_wu_stream(sensor, pin_index=0)

    stream.read_data_stream(max_timeout_count=None,
                            loop=loop,
                            callback=determine_wu_direction,
                            console=False)
    return stream


def read_with_polling(sensor, loop):
    count = 0
    try:
        while count < loop or loop is None:

            if sensor.read_register(r.KXTJ2_INT_SOURCE1)[0] & b.KXTJ2_INT_SOURCE1_WUFS != 0:
                int_source2 = sensor.read_register(r.KXTJ2_INT_SOURCE2)[0]
                print ('WAKEUP DETECTION polling mode:' +
                       wu_bits_to_str(int_source2))
                sensor.release_interrupts()
                time.sleep(1)
                count += 1

    except (KeyboardInterrupt):
        pass


def app_main():
    sensor = kxtj2_driver()
    bus = open_bus_or_exit(sensor)

    # wu interrupt hard coded to int2
    enable_wakeup(sensor,
                  cfg=Parameter_set_1)
    args = get_datalogger_args() 
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()


if __name__ == '__main__':
    app_main()
