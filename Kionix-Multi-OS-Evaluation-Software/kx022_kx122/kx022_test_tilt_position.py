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
""" Orientation Detection (ORI) is integrated feature for display
 rotation application

 MAIN REGISTER PARAMETERS
 Angle parameters are scaled to 2g measurement range
      TILT_ANGLE_LL is (according component's coordinate) threshold angle from currently detected position to another position
      TILT_ANGLE_HL is "transient angle" prevention threshold during rotating motion. Helpful parameter if timer value is short
      HYST_SET is +/-addenum to TILT_ANGLE_LL to prevent detection vibration
 TILT_TIMER is time * (1/OTP); how many sample must be valid until accepted
 OTP is selection of function dedicated ODR(Hz)
 CNTL2, bits LEM, RIM, DOM, UPM, FDM and FUM are masks of x-, x+, y+, y-, z+ and z-

 practically, with example values:
 from horizontal direction (z+ or z- side top); threshold level (to horizontal level) is 30degrees
 from vertical direction (x+,  x-,  y+ or y- side top); threshold level (compared to horizontal level) is 30degrees (or 60 degrees from start)

 other parameters
      CNTL1, bit RES and LP_CNTL average value make effects to current consumption
      ODCNTL, bit OSAx and CNTL3, bits OWUFx, OTDTx make effect current consumption if selected ORD is higher than OTPx
      
For KX022 tilt detection works always with +-4g range
"""
_CODE_FORMAT_VERSION = 2.0
# Example app for tilt position detection
##
# tilt position detection uses interrupt int2
##

from imports import *


class Parameter_set_1:
    # default values
    TILT_TIMER_VALUE = 0x04  # Register's default value 0x00; timer = 0.0s
    # 0x04 is 0.32s with 12.5Hz OTP, this value
    # prevents detection vibration
    # Register's default value 0x0C; angles about 22 and 90-22=58 degrees
    TILT_ANGLE_LL_VALUE = 0x10
    # 0x10 = 30degrees maybe better value than default
    TILT_ANGLE_HL_VALUE = 0x2A    # Register's default value 0x2A; angle over 90 degrees
    # 0x2D maybe better
    # Register's default value; angle threshold addenum +15/-15 degrees
    HYST_SET_VALUE = 0x14
    LOW_POWER_MODE = False                  # low power or full resolution mode
    odr = 12.5
    lp_average = '16_SAMPLE_AVG'                       # This parameter not used in full power mode


class Parameter_set_2:
    # values for detecting tilt angle angles 25 degrees / 20 degrees
    TILT_TIMER_VALUE = 0x02                 # Register's default value 0x00; timer = 0.0s
    TILT_ANGLE_LL_VALUE = 0x0C              # 20deg is target angle
    TILT_ANGLE_HL_VALUE = 0x2D              # transient angle blocking
    HYST_SET_VALUE = 0x09                   # hysteresis ~5 degrees
    LOW_POWER_MODE = False                  # low power or full resolution mode
    odr = 12.5
    lp_average = '16_SAMPLE_AVG'                       # This parameter not used in full power mode

class Parameter_set_3:
    # values for detecting tilt angle angles 25 degrees / 20 degrees, low power
    TILT_TIMER_VALUE = 0x02                 # Register's default value 0x00; timer = 0.0s
    TILT_ANGLE_LL_VALUE = 0x0C              # 20deg is target angle
    TILT_ANGLE_HL_VALUE = 0x2D              # transient angle blocking
    HYST_SET_VALUE = 0x09                   # hysteresis ~5 degrees
    LOW_POWER_MODE = True                   # low power or full resolution mode
    lp_average          = '16_SAMPLE_AVG'   # how many samples averaged in low power mode
    odr = 12.5

# native / rotated directions
resultResolverToString = {
    b.KX022_TSCP_LE:  "x-",
    b.KX022_TSCP_RI:  "x+",
    b.KX022_TSCP_DO:  "y-",
    b.KX022_TSCP_UP:  "y+",
    b.KX022_TSCP_FD:  "z-",
    b.KX022_TSCP_FU:  "z+"}


class kx022_tilt_stream(stream_config):

    def __init__(self, sensor, pin_index=1):
        stream_config.__init__(self, sensor)
        assert pin_index in [0, 1]

        self.define_request_message(
            fmt="BBBBBBBB",
            hdr="ch!TSCP!INS1!INS2!INS3!STATUS!NA!INT_REL",
            reg=r.KX022_TSCP,
            pin_index=pin_index)


def enable_tilt_position(sensor,
                         direction_mask=b.KX022_CNTL2_LEM |  # x- tilt direction mask
                         b.KX022_CNTL2_RIM |  # x+ tilt direction mask
                         b.KX022_CNTL2_DOM |  # y- tilt direction mask
                         b.KX022_CNTL2_UPM |  # y+ tilt direction mask
                         b.KX022_CNTL2_FDM |  # z- tilt direction mask
                         b.KX022_CNTL2_FUM,  # z+ tilt direction mask
                         cfg=Parameter_set_1,
                         power_off_on=True       # set to false if this function is part of other configuration
                         ):

    logger.info('Tilt position detection init start')

    #
    # parameter validation
    #

    # FIXME check which int pins are supported in selected HW
    assert convert_to_enumkey(cfg.odr) in e.KX022_ODCNTL_OSA.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    cfg.odr,e.KX022_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr) in e.KX022_CNTL3_OTDT.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    cfg.odr,e.KX022_CNTL3_OTDT.keys())
    
    assert cfg.lp_average in e.KX022_LP_CNTL_AVC.keys(),\
    'Invalid lp_average value "{}". Valid values are {}'.format(
    cfg.lp_average,e.KX022_LP_CNTL_AVC.keys())
    
    assert cfg.LOW_POWER_MODE in [True, False],\
    'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
    cfg.LOW_POWER_MODE,[True,False])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #
    # g-range is fixed +-4g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # enable low current mode
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)
        # define averaging value
        sensor.set_average(e.KX022_LP_CNTL_AVC[cfg.lp_average])
    else:
        # full resolution
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)

    # enable tilt position engine
    sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_TPE)

    # stream odr (if stream odr is biggest odr, it makes effect to current
    # consumption)
    sensor.set_odr(e.KX022_ODCNTL_OSA[convert_to_enumkey(cfg.odr)])
    # Set tilt detection odr
    sensor.set_bit_pattern(r.KX022_CNTL3, e.KX022_CNTL3_OTP[
                           convert_to_enumkey(cfg.odr)], m.KX022_CNTL3_OTP_MASK)

    #
    # Init tilt detection engine
    #

    # tilt direction definition
    sensor.write_register(r.KX022_CNTL2, direction_mask)

    sensor.write_register(r.KX022_TILT_TIMER,
                          cfg.TILT_TIMER_VALUE)             # Tilt timer
    # lower tilt angle threshold
    sensor.write_register(r.KX022_TILT_ANGLE_LL, cfg.TILT_ANGLE_LL_VALUE)
    # higher tilt angle threshold
    sensor.write_register(r.KX022_TILT_ANGLE_HL, cfg.TILT_ANGLE_HL_VALUE)
    # angle hysteresis
    sensor.write_register(r.KX022_HYST_SET, cfg.HYST_SET_VALUE)

    #
    # interrupt pin routings and settings
    #

    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin=2, polarity=ACTIVE_LOW)

    # enable tilt detection to int 2
    sensor.set_bit(r.KX022_INC6, b.KX022_INC6_TPI2)
    # latched interrupt 2
    sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)
    # enable int2 pin
    sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEN2)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('Tilt position event initialized.')


def determine_tilt_position(data):
    channel, tscp, tspp, ins1, ins2, ins3, status, rel = data
    print ('TILT_POSITION streaming mode:' + resultResolverToString[tscp])
    return True  # Continue reading


def read_with_stream(sensor, loop):
    # Note : pin_index = 0 == int_pin = 1
    stream = kx022_tilt_stream(sensor)
    stream.read_data_stream(max_timeout_count=None,
                            loop=loop,
                            callback=determine_tilt_position,
                            console=False)
    return stream


def read_with_polling(sensor, loop):
    "Monitor tilt position using either int2 or INS2/TPS"
    count = 0
    pin_condition = 0
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        pin_condition = 1

    try:
        while count < loop or loop is None:
            # check tilt event
            if evkit_config.get('generic', 'use_adapter_int_pins') == 'TRUE':
                # Read int pin
                tps = sensor._bus.poll_gpio(2) == pin_condition
            else:
                # Read interrupt register
                tps = sensor.read_register(r.KX022_INS2, 1)[
                    0] & b.KX022_INS2_TPS > 0

            if tps != 0:
                count += 1
                # Read interrupt source register
                tilt_direction = sensor.read_register(r.KX022_TSCP)[0]
                print ('TILT_POSITION polling mode:' +
                       resultResolverToString[tilt_direction])
                sensor.release_interrupts()             # clear all interrupts

    except(KeyboardInterrupt):
        pass


def app_main():
    sensor = kx022_driver()
    bus = open_bus_or_exit(sensor)

    enable_tilt_position(sensor,
                         cfg=Parameter_set_1)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()
