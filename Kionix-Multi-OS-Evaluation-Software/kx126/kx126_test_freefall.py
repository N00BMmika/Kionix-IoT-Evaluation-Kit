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
## Example app for freefall detection
### KX126
## Freefall detection uses interrupt intx
###
_CODE_FORMAT_VERSION = 2.0
from imports import *
from lib.data_stream import stream_config

class Parameter_set_1:
    LOW_POWER_MODE              = False
    odr_OSA                     = 25
    odr_OFFI                    = 100
    lp_average                  = '16_SAMPLE_AVG'
    FF_THRESHOLD_VALUE          = 8                                 # threshold
    FF_COUNTER_VALUE            = 5                                 # timer (100Hz)

class kx126_ff_stream(stream_config):

    def __init__(self, sensor, pin_index=1):
        stream_config.__init__(self, sensor)
        assert pin_index in [0, 1]

        self.define_request_message(
            fmt="BBBBBBB",
            hdr="ch!INS2!INS3!STATUS!INT_REL",
            reg=[sensor.address(), r.KX126_INS2,5, \
                 sensor.address(), r.KX126_INT_REL, 1,], \
            pin_index=pin_index)
    
def disable_freefall(sensor):
    sensor.reset_bit(r.KX126_FFCNTL, b.KX126_FFCNTL_FFIE)         # freefall disable

def enable_freefall(sensor,
                    cfg = Parameter_set_1,
                    int_pin = 2,
                    power_off_on = True):
    
    logger.info('Freefall event init start')            
    #
    # parameter validation
    #
    
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
    'Invalid odr_OSA value "{}". Valid values are {}'.format(
    cfg.odr_OSA, e.KX126_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr_OFFI) in e.KX126_FFCNTL_OFFI.keys(), \
    'Invalid odr_OFFI value "{}". Valid values are {}'.format(
    cfg.odr_OFFI,e.KX126_FFCNTL_OFFI.keys())
    
    assert cfg.LOW_POWER_MODE in [True,False],\
    'Invalid cfg.LOW_POWER_MODE value "{}". Valid values are {}'.format(
    cfg.LOW_POWER_MODE,[True, False])
    
    assert cfg.lp_average in e.KX126_LP_CNTL_AVC.keys(), \
    'Invalid lp_average value "{}". Valid values are {}'.format(
    cfg.lp_average, e.KX126_LP_CNTL_AVC.keys())
     
    # Sensor set to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()           

    #
    #Configure sensor
    #
    
    ## stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])         # odr setting for basic data logging

    # g-range is fixed +-8g
   
    ## resolution / power mode selection
    ## Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)  
    if cfg.LOW_POWER_MODE:
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                      # low current
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])                 # lowest current mode average
    else:
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                        # high resolution

    # Free fall setup 
    sensor.set_bit(r.KX126_FFCNTL, b.KX126_FFCNTL_FFIE)             # freefall enable
    sensor.set_bit(r.KX126_FFCNTL, b.KX126_FFCNTL_ULMODE)           # latched int
    sensor.set_bit(r.KX126_FFCNTL, b.KX126_FFCNTL_DCRM)
    sensor.set_bit_pattern(r.KX126_FFCNTL, \
                           e.KX126_FFCNTL_OFFI[convert_to_enumkey(cfg.odr_OFFI)], \
                           m.KX126_FFCNTL_OFFI_MASK)                # freefall odr
    sensor.write_register(r.KX126_FFTH, cfg.FF_THRESHOLD_VALUE)     # freefall threshold
    sensor.write_register(r.KX126_FFC, cfg.FF_COUNTER_VALUE)        # freefal timer

    ## interrupt pin and visibility
    if int_pin == 1:
        sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEL1)           # int1 latched interrupt           
        if evkit_config.get('generic','int1_active_high') == 'TRUE':
            sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEA1)         # int1 active high
        else:
            sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEA1)       # int1 active low
        sensor.set_bit(r.KX126_INC4, b.KX126_INC4_FFI1)             # freefall to int1 pin        
        sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEN1)             # enable int1    
    else:  # int_pin==2
        sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2)           # int2 latched interrupt           
        if evkit_config.get('generic','int2_active_high') == 'TRUE':
            sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEA2)         # int2 active high
        else:
            sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEA2)       # int2 active low
        sensor.set_bit(r.KX126_INC6, b.KX126_INC6_FFI2)             # freefall to int2 pin        
        sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)             # enable int2        
        
    # Turn on operating mode (disables setup)
    if power_off_on:
        sensor.set_power_on()                                   # Turn on operating mode (disables setup)
    
    #sensor.register_dump()#;sys.exit()

    logger.info('\nFreefall detection enabled')

    sensor.release_interrupts()                                 # clear all internal function interrupts

def determine_int_pin(sensor):              # find int pin routing for free fall
    int_pin = 0
    if sensor.read_register(r.KX126_INC4, 1)[0] & b.KX126_INC4_FFI1 > 0:
        int_pin = 1
    if sensor.read_register(r.KX126_INC6, 1)[0] & b.KX126_INC6_FFI2 > 0:
        int_pin = 2
    return int_pin

def determine_ff_status(data):
    channel, ins2, ins3, stat,na1,na2, int_rel = data    
    print 'FREE FALL streaming mode: ', ins2 & b.KX126_INS2_FFS > 0
    time.sleep(0.3)
    return True  # Continue reading

def read_with_stream(sensor, loop):
    # Note : pin_index = 0 == int_pin = 1
    stream = kx126_ff_stream(sensor, pin_index=1) # FIXME! pin_index as parameter
    stream.read_data_stream(max_timeout_count=None,
                            loop=loop,
                            callback=determine_ff_status,
                            console=False)

def read_with_polling(sensor, loop):
    count = 0
    int_pin = determine_int_pin(sensor)

    pin_condition = 0
    if int_pin == 1:
        if evkit_config.get('generic','int1_active_high')=='TRUE':
            pin_condition = 1
    else:
        if evkit_config.get('generic','int2_active_high')=='TRUE':
            pin_condition = 1
            
    ffs_event = False

    try:
        while count < loop or loop is None:

            if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':
                ffs_event = sensor._bus.poll_gpio(int_pin) == pin_condition
            else:
                ffs_event = sensor.read_register(r.KX126_INS2)[0] & b.KX126_INS2_FFS  > 0

            if ffs_event:
                count += 1
                if loop == None or loop < count:
                    print 'Free Fall activity detected:'
                time.sleep(0.3)
                ffs_event = False
                sensor.release_interrupts()                         # clear all interrupts
                
    except KeyboardInterrupt:
        pass
    
def app_main():
    sensor = kx126_driver()
    bus = open_bus_or_exit(sensor)

    enable_freefall(sensor,
                    cfg=Parameter_set_1,
                    int_pin = 2) 
    args = get_datalogger_args()   
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    disable_freefall(sensor)    
    sensor.set_power_off()
    bus.close()
        
if __name__ == '__main__':
    app_main()
