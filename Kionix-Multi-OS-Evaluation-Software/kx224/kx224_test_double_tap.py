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
Double tap detection.
For KX224 double tap detection works always with +-16g range
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *


class Parameter_set_1:
    """Tap sensitivity for 400Hz, no averaging (Normal power)"""

    TAP_TTL             = [0x7E, 0x46, 0x2A]                #
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ### tap values              # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX224_TDTC_VALUE    = 0x78  # 0x78  #       #       #       #           # timer value 1/400Hz, 2,5ms tick => 0,3s
    KX224_TTH_VALUE     = 0xCB  # 0xCB  #       #       #       #           # threshold high (0,0078) 3.08g in 4g range
    KX224_TTL_VALUE     = TAP_TTL[SENSITIVITY]       
                                # 0x2A  #       #       #       #           # threshold low (0.81g in 4g range)
    KX224_FTD_VALUE     = 0xA2  # 0xA2  #       #       #       #           # timer (default A2h) (0.025s, 2.5ms tick)
    KX224_STD_VALUE     = 0x24  # 0x24  #       #       #       #           # time (default 24h) (0.09s, 2.5ms tick) - TTL
    KX224_TLT_VALUE     = 0x28  # 0x28  #       #       #       #           # timer(default 28h) (0.1s, 2.5ms)
    KX224_TWS_VALUE     = 0xA0  # 0xA0  #       #       #       #           # time (default A0h) (0.4s, 2.5ms)
    odr_OTDT            = 400
    odr_OSA             = 400
    LOW_POWER_MODE      = False                                             # low power or full resolution mode
    lp_average          = '2_SAMPLE_AVG'                                    # how many samples averaged in low power mode
    
class Parameter_set_2:
    """Tap sensitivity for 2g, 100Hz, 2sample average (light hand, low power)"""

    TAP_TTL             = [0xA4, 0x92, 0x82]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity

    # light tap values        # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX224_TDTC_VALUE    = 0x0B  #       #       # 0x0E  #       #
    KX224_TTH_VALUE     = 0xEB  #       #       # 0xEB  #       #
    KX224_TTL_VALUE     = TAP_TTL[SENSITIVITY]
                                #       #       # 0x82  #       #
    KX224_FTD_VALUE     = 0x15  #       #       # 0x15  #       #
    KX224_STD_VALUE     = 0x12  #       #       # 0x12  #       #
    KX224_TLT_VALUE     = 0x09  #       #       # 0x09  #       #
    KX224_TWS_VALUE     = 0x22  #       #       # 0x22  #       #
    odr_OTDT            = 100
    odr_OSA             = 100
    LOW_POWER_MODE      = True                                  # low power or full resolution mode
    lp_average          = '2_SAMPLE_AVG'                        # how many samples averaged in low power mode

class Parameter_set_3:
    """Tap sensitivity for 4g, 100Hz, 1 sample average (heavy hand, low power)"""
    TAP_TTL             = [0xB4, 0xA2, 0x92]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ## low power
    ## tap values                                            400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX224_TDTC_VALUE = 0x1E                # timer value    0x78  # 0x3C  # 0x1E  # 0x11  # 0x0D
    KX224_TTH_VALUE  = 0xDB                # threshold high 0xCB  # 0xDB  # 0xDB  # 0xDB  # 0xDB
    KX224_TTL_VALUE  = TAP_TTL[SENSITIVITY]
                                            # threshold low  0xA2  # 0xA2  # 0x92  # 0x52  # 0x42
    KX224_FTD_VALUE  = 0x17                # timer          0x2A  # 0x19  # 0x17  # 0x15  # 0x02
    KX224_STD_VALUE  = 0x12                # timer          0x24  # 0x1A  # 0x12  # 0x05  # 0x03
    KX224_TLT_VALUE  = 0x0b                # timer          0x28  # 0x1F  # 0x0B  # 0x06  # 0x04
    KX224_TWS_VALUE  = 0x28                # timer          0xA0  # 0x50  # 0x28  # 0x13  # 0x0C
    odr_OTDT            = 100
    odr_OSA             = 100
    LOW_POWER_MODE      = True                                          # low power or full resolution mode
    lp_average          = 'NO_AVG'                                   # how many samples averaged in low power mode

# native / rotated directions
resultResolverToString = {
    b.KX224_INS1_TLE:  "x-",
    b.KX224_INS1_TRI:  "x+",
    b.KX224_INS1_TDO:  "y-",
    b.KX224_INS1_TUP:  "y+",
    b.KX224_INS1_TFD:  "z-",
    b.KX224_INS1_TFU:  "z+"}


class kx224_dt_stream(stream_config):

    def __init__(self, sensor, pin_index=1):
        stream_config.__init__(self, sensor)
        assert pin_index in [0, 1]

        self.define_request_message(
            fmt="BBBBBBB",
            hdr="ch!INS1!INS2!INS3!STATUS!NA!INT_REL",
            reg=r.KX224_INS1,
            pin_index=pin_index)


def enable_double_tap(sensor,
                      direction_mask=b.KX224_INC3_TLEM |  # x- left set
                      b.KX224_INC3_TRIM |  # x+ right set
                      b.KX224_INC3_TDOM |  # y- back set
                      b.KX224_INC3_TUPM |  # y+ front set
                      b.KX224_INC3_TFDM |  # z- down set
                      b.KX224_INC3_TFUM,  # z+ up set
                      cfg=Parameter_set_1,
                      int_pin=2,
                      power_off_on=True       # set to False if this function is part of other configuration
                      ):

    logger.info('Double tap event init start')

    #
    # parameter validation
    #

    # FIXME check which int pins are supported in selected HW
    assert int_pin in[1,2]
    
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX224_ODCNTL_OSA.keys(),\
    'Invalid odr_OSA value "{}". Valid values are {}'.format(
    cfg.odr_OSA,e.KX224_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr_OTDT) in e.KX224_CNTL3_OTDT.keys(),\
    'Invalid odr_OTDT value "{}". Valid values are {}'.format(
    cfg.odr_OTDT,e.KX224_CNTL3_OTDT.keys())
    
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
    #Configure sensor
    #

    # g-range is fixed +-16g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # low current
        sensor.reset_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)
        # set averaging (only for low power)
        sensor.set_average(e.KX224_LP_CNTL_AVC[cfg.lp_average])
    else:
        # full resolution
        sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)

    # enable double tap detection engine
    sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_TDTE)

    # stream odr (if stream odr is biggest odr, it makes effect to current
    # consumption)
    sensor.set_odr(e.KX224_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])
    # Set tap detection odr
    sensor.set_bit_pattern(r.KX224_CNTL3, e.KX224_CNTL3_OTDT[
                           convert_to_enumkey(cfg.odr_OTDT)], m.KX224_CNTL3_OTDT_MASK)
    #
    # Init tap detection engine
    #

    # tap direction definition
    sensor.write_register(r.KX224_INC3, direction_mask)

    # Disable single tap and enable double tap interrupt
    sensor.reset_bit(r.KX224_TDTRC, b.KX224_TDTRC_STRE)
    sensor.set_bit(r.KX224_TDTRC,   b.KX224_TDTRC_DTRE)

    # TDTC: Counter information for the detection of a double tap event.
    # 1/400Hz (0.3s, 2.5ms)
    sensor.write_register(r.KX224_TDTC, cfg.KX224_TDTC_VALUE)

    # TTH: High threshold jerk value for tap functions
    sensor.write_register(r.KX224_TTH, cfg.KX224_TTH_VALUE)

    # TTL: Low threshold jerk value for tap functions
    sensor.write_register(r.KX224_TTL, cfg.KX224_TTL_VALUE)

    # FTD: Timer settings for tap signal.
    sensor.write_register(r.KX224_FTD, cfg.KX224_FTD_VALUE)

    # STD: Timer for two taps signal above threshold
    sensor.write_register(r.KX224_STD, cfg.KX224_STD_VALUE)

    # TLT: Timer calculates samples above threshold
    sensor.write_register(r.KX224_TLT, cfg.KX224_TLT_VALUE)

    # TWS: TImer for tap function event
    sensor.write_register(r.KX224_TWS, cfg.KX224_TWS_VALUE)

    #
    # interrupt pin routings and settings
    #

    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin=int_pin, polarity=ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin=int_pin, polarity=ACTIVE_LOW)

    if int_pin == 1:
        # enable double tap detection to int1
        sensor.set_bit(r.KX224_INC4, b.KX224_INC4_TDTI1)
        # latched interrupt 1
        sensor.reset_bit(r.KX224_INC1, b.KX224_INC1_IEL1)
        # enable int1 pin
        sensor.set_bit(r.KX224_INC1, b.KX224_INC1_IEN1)

    else:  # int_pin==2
        # enable double tap detection to int2
        sensor.set_bit(r.KX224_INC6, b.KX224_INC6_TDTI2)
        # latched interrupt 2
        sensor.reset_bit(r.KX224_INC5, b.KX224_INC5_IEL2)
        # enable int2 pin
        sensor.set_bit(r.KX224_INC5, b.KX224_INC5_IEN2)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('Double tap event initialized.')


def determine_tap_direction(data):
    channel,  ins1, ins2, ins3, status, NA, rel = data
    print ('TAP detectedstreaming mode: ' + resultResolverToString[ins1])
    return True  # Continue reading


def read_with_stream(sensor, loop):
    # Note : pin_index = 0 == int_pin = 1
    stream = kx224_dt_stream(sensor, pin_index=1)
    stream.read_data_stream(max_timeout_count=None,
                            loop=loop,
                            callback=determine_tap_direction,
                            console=False)
    return stream


def read_with_polling(sensor, loop):
    "Monitor double tap using either int2 or INS/TDTS"
    count = 0
    pin_condition = 0
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        pin_condition = 1

    try:
        while count < loop or loop is None:
            # check tilt event
            if evkit_config.get('generic', 'use_adapter_int_pins') == 'TRUE':
                # Read int pin
                tap_event = sensor._bus.poll_gpio(2) == pin_condition
            else:
                # Read interrupt register
                tap_event = sensor.read_register(
                    r.KX224_INS2)[0] & b.KX224_INS2_TDTS_DOUBLE > 0

            if tap_event != 0:
                count += 1
                # Read interrupt source register
                tap_direction = sensor.read_register(r.KX224_INS1)[0]
                print ('TAP detected polling mode: ' +
                       resultResolverToString[tap_direction])
                sensor.release_interrupts()             # clear all interrupts

    except(KeyboardInterrupt):
        pass


def app_main():
    sensor = kx224_driver()
    bus = open_bus_or_exit(sensor)

    enable_double_tap(sensor,
                      cfg=Parameter_set_1,
                      int_pin=2)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()
