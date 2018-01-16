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
'''
Example app for basic taptap detection

Double tap uses interrupt int1
'''
_CODE_FORMAT_VERSION = 2.0
from imports import *



#############################################
class Parameter_set_1:
    # Tap sensitivity for 400Hz, no averaging (Normal power)
    LOW_POWER_MODE      = False
    odr_OSA             = 25
    odr_OTDT            = 400
    lp_average          = '16_SAMPLE_AVG'
    TAP_TTL             = [0x7E, 0x46, 0x2A]                #
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ### tap values              # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTC_VALUE    = 0x78  # 0x78  #       #       #       #           # timer value 1/400Hz, 2,5ms tick => 0,3s
    KX126_TTH_VALUE     = 0xCB  # 0xCB  #       #       #       #           # threshold high (0,0078) 3.08g in 4g range
    KX126_TTL_VALUE     = TAP_TTL[SENSITIVITY]       
                                # 0x2A  #       #       #       #           # threshold low (0.81g in 4g range)
    KX126_FTD_VALUE     = 0xA2  # 0xA2  #       #       #       #           # timer (default A2h) (0.025s, 2.5ms tick)
    KX126_STD_VALUE     = 0x24  # 0x24  #       #       #       #           # time (default 24h) (0.09s, 2.5ms tick) - TTL
    KX126_TLT_VALUE     = 0x28  # 0x28  #       #       #       #           # timer(default 28h) (0.1s, 2.5ms)
    KX126_TWS_VALUE     = 0xA0  # 0xA0  #       #       #       #           # time (default A0h) (0.4s, 2.5ms)

#############################################
class Parameter_set_2:
    # Tap sensitivity for 2g, 100Hz, 2sample average (light hand, low power)
    LOW_POWER_MODE      = True
    odr_OSA             = 25
    odr_OTDT            = 100
    lp_average          = '2_SAMPLE_AVG'
    TAP_TTL             = [0xA4, 0x92, 0x82]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity

    ## light tap values        # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTC_VALUE    = 0x0B  #       #       # 0x0E  #       #
    KX126_TTH_VALUE     = 0xEB  #       #       # 0xEB  #       #
    KX126_TTL_VALUE     = TAP_TTL[SENSITIVITY]
                                      #       # 0x82  #       #
    KX126_FTD_VALUE     = 0x15  #       #       # 0x15  #       #
    KX126_STD_VALUE     = 0x12  #       #       # 0x12  #       #
    KX126_TLT_VALUE     = 0x09  #       #       # 0x09  #       #
    KX126_TWS_VALUE     = 0x22  #       #       # 0x22  #       #
class Parameter_set_3:
    # alternate settings for heavy hand #######
    # Tap sensitivity for 4g, 100Hz, 1 sample average (heavy hand, low power)
    LOW_POWER_MODE      = True
    odr_OSA             = 25
    odr_OTDT            = 100
    lp_average          = 'NO_AVG'
    TAP_TTL             = [0xB4, 0xA2, 0x92]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    # tap values                                            400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTC_VALUE = 0x1E                # timer value    0x78  # 0x3C  # 0x1E  # 0x11  # 0x0D
    KX126_TTH_VALUE  = 0xDB                # threshold high 0xCB  # 0xDB  # 0xDB  # 0xDB  # 0xDB
    KX126_TTL_VALUE  = TAP_TTL[SENSITIVITY]
                                           # threshold low  0xA2  # 0xA2  # 0x92  # 0x52  # 0x42
    KX126_FTD_VALUE  = 0x17                # timer          0x2A  # 0x19  # 0x17  # 0x15  # 0x02
    KX126_STD_VALUE  = 0x12                # timer          0x24  # 0x1A  # 0x12  # 0x05  # 0x03
    KX126_TLT_VALUE  = 0x0b                # timer          0x28  # 0x1F  # 0x0B  # 0x06  # 0x04
    KX126_TWS_VALUE  = 0x28                # timer          0xA0  # 0x50  # 0x28  # 0x13  # 0x0C

# native / rotated directions
resultResolverToString = {
    b.KX126_INS1_TLE:  "x-",
    b.KX126_INS1_TRI:  "x+",
    b.KX126_INS1_TDO:  "y-",
    b.KX126_INS1_TUP:  "y+",
    b.KX126_INS1_TFD:  "z-",
    b.KX126_INS1_TFU:  "z+" }

##########################################
# Enabler methods for asic features
def enable_double_tap(sensor,
                        cfg = Parameter_set_1,
                        power_off_on = True):
                        
    logger.info('Double tap event init start')                    
    
    #
    # parameter validation
    #
    
    assert cfg.LOW_POWER_MODE in [True, False],\
    'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
    cfg.LOW_POWER_MODE,[True,False])
    
    assert cfg.lp_average in e.KX126_LP_CNTL_AVC.keys(), \
    'Invalid lp_average value "{}". Valid values are {}'.format(
    cfg.lp_average,e.KX126_LP_CNTL_AVC.keys())
    
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
    'Invalid odr_OSA value "{}". Valid values are {}'.format(
    cfg.odr_OSA,e.KX126_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr_OTDT) in e.KX126_CNTL3_OTDT.keys()
    'Invalid odr_OTDT value "{}". Valid values are {}'.format(
    cfg.odr_OTDT,e.KX126_CNTL3_OTDT.keys())
    
    
    # Sensor set to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settingsSet sensor to stand-by to enable setup change   

    #
    #Configure sensor
    #
    # g-range is fixed +-4g

    ## resolution / power mode selection
    ## Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)  
    if cfg.LOW_POWER_MODE:
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                          # low current
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])                     # lowest current mode average
    else:
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                            # high resolution

    ## Set double tap bit on
    sensor.set_bit(r.KX126_CNTL1,b.KX126_CNTL1_TDTE)
    
    ## Set tap odr
    sensor.write_register(r.KX126_CNTL3, 0)         # all odrs to minimum first
    sensor.set_bit_pattern(r.KX126_CNTL3, e.KX126_CNTL3_OTDT[convert_to_enumkey(cfg.odr_OTDT)], m.KX126_CNTL3_OTDT_MASK)

    ##stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])         
    
    #
    # Init tap detection engine
    #
    
    ## Init tap directions
    sensor.write_register(r.KX126_INC3, 0)          # all off, default is all on
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TLEM)  # x- left set
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TRIM)  # x+ right set
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TDOM)  # y- back set
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TUPM)  # y+ front set
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TFDM)  # z- down set
    sensor.set_bit(r.KX126_INC3,b.KX126_INC3_TFUM)  # z+ up set

    ## Disable single tap and enable double tap interrupt
    sensor.reset_bit(r.KX126_TDTRC, b.KX126_TDTRC_STRE)
    sensor.set_bit(r.KX126_TDTRC,   b.KX126_TDTRC_DTRE)

    ## TDTC: Counter information for the detection of a double tap event. 1/400Hz (0.3s, 2.5ms)
    sensor.write_register(r.KX126_TDTC,cfg.KX126_TDTC_VALUE)

    ## TTH: High threshold jerk value for tap functions
    sensor.write_register(r.KX126_TTH,cfg.KX126_TTH_VALUE)

    ## TTL: Low threshold jerk value for tap functions
    sensor.write_register(r.KX126_TTL,cfg.KX126_TTL_VALUE)

    ## FTD: Timer settings for tap signal.
    sensor.write_register(r.KX126_FTD,cfg.KX126_FTD_VALUE)

    ## STD: Timer for two taps signal above threshold
    sensor.write_register(r.KX126_STD,cfg.KX126_STD_VALUE)

    ## TLT: Timer calculates samples above threshold
    sensor.write_register(r.KX126_TLT, cfg.KX126_TLT_VALUE)

    ## TWS: TImer for tap function event
    sensor.write_register(r.KX126_TWS,cfg.KX126_TWS_VALUE)
     
    ## interrupt pin routings and settings  
    ## interrupt signal parameters
    sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEL1)  # latched interrupt
    assert evkit_config.get('generic','int1_active_high') in ['TRUE','FALSE']    
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEA1) # active high
    else:
        sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEA1)# active low

    sensor.set_bit(r.KX126_INC4, b.KX126_INC4_TDTI1)     # double tap to int1
    sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEN1)       # enable int1 pin
    
    #    
    # Turn on operating mode (disables setup)
    #
    if power_off_on:
        sensor.set_power_on()                               # settings coming to valid and start measurements
    
    #sensor.register_dump()    
    
    logger.info('\nDouble tap event initialized.')
    
    sensor.release_interrupts()                         # clear all internal function interrupts

def read_with_polling(sensor):
    tap_event = False
    pin_condition = 0
    if evkit_config.get('generic','int1_active_high')=='TRUE':
        pin_condition = 1

    try:
        while 1:
            if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':
                tap_event = sensor._bus.poll_gpio(1) == pin_condition
            else:
                tap_event = sensor.read_register(r.KX126_INS2)[0] & b.KX126_INS2_TDTS_DOUBLE > 0

            if tap_event:
                tap_direction = sensor.read_register(r.KX126_INS1)[0]
                print 'Direction   ', tap_direction
                print 'DOUBLE_TAP: ', resultResolverToString[tap_direction]
                sensor.release_interrupts()             # clear all internal function interrupts
                tap_event = False                       # new round
                    
    except(KeyboardInterrupt):
        pass
    
    finally:
        logger.info('bye')
def app_main():
    sensor = kx126_driver()
    bus = open_bus_or_exit(sensor)
    try:
        enable_double_tap(sensor)
        read_with_polling(sensor)
    finally:
        sensor.set_power_off()
        bus.close()
if __name__ == '__main__':
    app_main()
