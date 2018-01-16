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
Wakeup uses interrupt int2
For KX224 wakeup detection works always with +-32g range
"""

_CODE_FORMAT_VERSION = 2.0
from imports import *


class Parameter_set_1:
    # low power, low odr
    LOW_POWER_MODE = True           # low power or full resolution mode
    WUFC_VALUE = 0x00              # wakeup control timer
    ATH_VALUE = 0x0a              # threshold for wakeup
    odr_OSA = 3.125                # ODR for sensor
    odr_OWUF = 3.125
    lp_average = '16_SAMPLE_AVG'   # how many samples averaged in low power mode

# native / rotated directions
resultResolverToString = {
    b.KX224_INS3_XNWU:  "x-",
    b.KX224_INS3_XPWU:  "x+",
    b.KX224_INS3_YNWU:  "y-",
    b.KX224_INS3_YPWU:  "y+",
    b.KX224_INS3_ZNWU:  "z-",
    b.KX224_INS3_ZPWU:  "z+"}


class kx224_wu_stream(stream_config):

    def __init__(self, sensor, pin_index=1):
        stream_config.__init__(self, sensor)
        assert pin_index in [0, 1]

        self.define_request_message(
            fmt="BBBBBBB",
            hdr="ch!INS1!INS2!INS3!STATUS!NA!INT_REL",
            reg=r.KX224_INS1,
            pin_index=pin_index)


def enable_wakeup(sensor,
                  direction_mask=b.KX224_INC2_XNWUE |      # x- direction mask
                  b.KX224_INC2_XPWUE |      # x+ direction mask
                  b.KX224_INC2_YNWUE |      # y- direction mask
                  b.KX224_INC2_YPWUE |      # y+ direction mask
                  b.KX224_INC2_ZNWUE |      # z- direction mask
                  b.KX224_INC2_ZPWUE,      # z+ direction mask
                  cfg=Parameter_set_1,
                  power_off_on=True       # set to False if this function is part of other configuration
                  ):

    logger.info('Wakeup event init start')

    #
    # parameter validation
    #

    
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX224_ODCNTL_OSA.keys(),\
    'Invalid odr_OSA value "{}". Valid values are {}'.format(
    cfg.odr_OSA,e.KX224_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr_OWUF) in e.KX224_CNTL3_OWUF.keys(),\
    'Invalid odr_OWUF value "{}". Valid values are {}'.format(
    cfg.odr_OWUF,e.KX224_CNTL3_OWUF.keys())
    
    assert cfg.lp_average in e.KX224_LP_CNTL_AVC.keys(),\
    'Invalid lp_average value "{}". Valid values are {}'.format(
    cfg.lp_average, e.KX224_LP_CNTL_AVC.keys())
    
    assert cfg.LOW_POWER_MODE in [True, False],\
    'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
    cfg.LOW_POWER_MODE,[True,False])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
        
    #
    # Configure sensor
    #

    # g-range is fixed +-32g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # low current
        sensor.reset_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)
        # set averaging (only for low power)
        sensor.set_average(e.KX224_LP_CNTL_AVC[cfg.lp_average])
    else:
        # full resolution
        sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)

    # enable wakeup detection engine
    sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_WUFE)
    # stream odr (if stream odr is biggest odr, it makes effect to current
    # consumption)
    sensor.set_odr(e.KX224_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])
    # Set wuf detection odr
    sensor.set_bit_pattern(r.KX224_CNTL3,
                           e.KX224_CNTL3_OWUF[convert_to_enumkey(cfg.odr_OWUF)],
                           m.KX224_CNTL3_OWUF_MASK)

    #
    # Init wuf detection engine
    #

    # WUF direction definition
    sensor.write_register(r.KX224_INC2, direction_mask)
    # WUF timer
    sensor.write_register(r.KX224_WUFC, cfg.WUFC_VALUE)
    # WUF threshold
    sensor.write_register(r.KX224_ATH, cfg.ATH_VALUE)

    sensor.set_bit_pattern(r.KX224_INC2, e.KX224_INC2_AOI[
                           'OR'], m.KX224_INC2_AOI_MASK)  # (POR default value)

    #
    # interrupt pin routings and settings
    #

    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_LOW)

    # enable wakeup detection to int2
    sensor.set_bit(r.KX224_INC6, b.KX224_INC6_WUFI2)
    # latched interrupt for int2
    sensor.reset_bit(r.KX224_INC5, b.KX224_INC5_IEL2)
    # enable int2 pin
    sensor.set_bit(r.KX224_INC5, b.KX224_INC5_IEN2)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('Wakeup event initialized.')


def wu_bits_to_str(ins3):
    "Convert content of ins3 register to movement directions"
    direction_list = []
    for i in range(0, 6):
        j = 0x01 << i
        if ins3 & j > 0:
            direction_list.append(resultResolverToString[j])

    return ' '.join(direction_list)


def determine_wu_direction(data):
    channel, ins1, ins2, ins3, status, NA, rel = data
    print ('WAKEUP DETECTION streming mode:' + wu_bits_to_str(ins3))
    return True  # Continue reading


def read_with_stream(sensor, loop):
    # Note pin_index = 0 == int_pin = 1
    stream = kx224_wu_stream(sensor, pin_index=1)

    stream.read_data_stream(max_timeout_count=None,
                            loop=loop,
                            callback=determine_wu_direction,
                            console=False)
    return stream


def read_with_polling(sensor, loop):
    count = 0
    pin_condition = 0
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        pin_condition = 1

    try:
        while count < loop or loop is None:

            # check wu event
            if evkit_config.get('generic', 'use_adapter_int_pins') == 'TRUE':
                # Read int pin
                wufs = sensor._bus.poll_gpio(2) == pin_condition
            else:
                # Read interrupt register
                wufs = sensor.read_register(r.KX224_INS2, 1)[
                    0] & b.KX224_INS2_WUFS > 0

            # Read wake up direction
            if wufs != 0:
                count += 1
                ins3 = sensor.read_register(r.KX224_INS3)[0]
                print ('WAKEUP DETECTION polling mode:' + wu_bits_to_str(ins3))
                sensor.release_interrupts()                         # clear all interrupts

    except (KeyboardInterrupt):
        pass


def app_main():
    sensor = kx224_driver()
    bus = open_bus_or_exit(sensor)

    # wu interrupt hard coded to int2
    enable_wakeup(sensor,
                  cfg=Parameter_set_1)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()
