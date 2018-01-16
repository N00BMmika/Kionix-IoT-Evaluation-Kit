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
freefall application

uses int1 for interrupt
'''
_CODE_FORMAT_VERSION = 2.0
from imports import *

class Parameter_set_1:
    LOW_POWER_MODE  = False
    odr_OSA         = 25
    odr_OSM         = 25
    odr_OFFI        = 100
    acc_range       = '2G'
    lp_average      = 'A32M16'
    FF_THRESHOLD_VALUE          = 10        # threshold
    FF_COUNTER_VALUE            = 5         # timer (100Hz)
    
class kmx62_ff_stream(stream_config):

    def __init__(self, sensor, pin_index=1):
        stream_config.__init__(self, sensor)
        assert pin_index in [0, 1]
        self.define_request_message(
            fmt="BBBBBB",
            hdr="ch!!INS1!INS2!INS3!INL",
            reg=[sensor.address(), r.KMX62_INS1, 4, \
                 sensor.address(), r.KMX62_INL, 1], \
            pin_index=pin_index)
              
def disable_freefall(sensor):
    sensor.reset_bit(r.KMX62_FFI_CNTL3, b.KMX62_FFI_CNTL3_FFI_EN_ENABLED)         # freefall disable

def enable_freefall(sensor,
                    cfg = Parameter_set_1,
                    int_pin = 1,                    
                    power_off_on = True):
                    
    logger.info('Freefall event init start')    
    #
    # parameter validation
    #
    
    assert convert_to_enumkey(cfg.odr_OSM) in e.KMX62_ODCNTL_OSM.keys(),\
    'Invalid odr_OSM value "{}". Support values are {}'.format(
    cfg.odr_OSM, e.KMX62_ODCNTL_OSM.keys())
    
    assert convert_to_enumkey(cfg.odr_OSA) in e.KMX62_ODCNTL_OSA.keys(),\
    'Invalid odr_OSA value "{}". Support values are {}'.format(
    cfg.odr_OSA,e.KMX62_ODCNTL_OSA.keys())
    
    assert cfg.lp_average in e.KMX62_CNTL2_RES.keys(),\
   'Invalid lp_mode value "{}". Support values are {} and False'.format(
    cfg.lp_average, e.KMX62_CNTL2_RES.keys())
            
    assert cfg.acc_range in e.KMX62_CNTL2_GSEL.keys(),\
    'Invalid acc_range value "{}". Support values are {}'.format(
    cfg.acc_range,e.KMX62_CNTL2_GSEL.keys())
    
    assert cfg.LOW_POWER_MODE in [True,False],\
    'Invalid LOW_POWER_MODE value "{}" valid values are {}'.format(
    cfg.LOW_POWER_MODE, [True,False])
    
    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
        
    #
    # Configure sensor
    #

    ##Select acc ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)], CH_ACC)                  # set acc stream ODR

    ##Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[convert_to_enumkey(cfg.odr_OSM)], CH_MAG)                  # set mag stream ODR

    ## select g-range (for acc)
    sensor.set_range(e.KMX62_CNTL2_GSEL[cfg.acc_range], None, CH_ACC)
    
    ## power mode (accelerometer and magnetometer)
    if cfg.LOW_POWER_MODE:
        ## Low power mode
        sensor.set_average(e.KMX62_CNTL2_RES[cfg.lp_average], None, CH_ACC)
    else:
        ## Full power mode
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2,None, CH_ACC)
        
    ## free fall setup
    sensor.set_bit(r.KMX62_FFI_CNTL3, b.KMX62_FFI_CNTL3_FFI_EN_ENABLED) # latched int    
    sensor.set_bit(r.KMX62_FFI_CNTL3, b.KMX62_FFI_CNTL3_FFIUL)          # latched int
    sensor.set_bit(r.KMX62_FFI_CNTL3, b.KMX62_FFI_CNTL3_DCRM)    
    sensor.write_register(r.KMX62_FFI_CNTL1, cfg.FF_THRESHOLD_VALUE)    # freefall threshold
    sensor.write_register(r.KMX62_FFI_CNTL2, cfg.FF_COUNTER_VALUE)      # freefall counter
    sensor.write_register(r.KMX62_FFI_CNTL3, b.KMX62_FFI_CNTL3_FFI_EN_ENABLED   | \
                                             e.KMX62_FFI_CNTL3_OFFI[convert_to_enumkey(cfg.odr_OFFI)] | \
                                             b.KMX62_FFI_CNTL3_FFIUL            | \
                                             b.KMX62_FFI_CNTL3_DCRM)    # FFI on + FFI odr + latch mode + debounce
    
    ## interrupts
    if int_pin == 1:    
        sensor.set_bit(r.KMX62_INC1, b.KMX62_INC1_FFI1)                     # freefall interrupt to int1
        if evkit_config.get('generic','int1_active_high') == 'TRUE':
            IEA1 = b.KMX62_INC3_IEA1_HIGH
        else:
            IEA1 = b.KMX62_INC3_IEA1_LOW
        sensor.write_register(r.KMX62_INC3, b.KMX62_INC3_IED1_PUSHPULL   | \
                                            IEA1                         | \
                                            b.KMX62_INC3_IEL1_LATCHED)      
    else:
        sensor.set_bit(r.KMX62_INC1, b.KMX62_INC2_FFI2)                     # freefall interrupt to int2
        if evkit_config.get('generic','int2_active_high') == 'TRUE':
            IEA2 = b.KMX62_INC3_IEA2_HIGH
        else:
            IEA2 = b.KMX62_INC3_IEA2_LOW
        sensor.write_register(r.KMX62_INC3, b.KMX62_INC3_IED2_PUSHPULL   | \
                                            IEA2                         | \
                                            b.KMX62_INC3_IEL2_LATCHED)      

    #
    # Turn on operating mode (disables setup)
    #
    ## power on sensor(s)
    if power_off_on:
        sensor.set_power_on(CH_ACC)                             # Accelerometer sensor standby->operating mode

    #sensor.register_dump()#;sys.exit()
        
    logger.info('\n Freefall detection enabled')
    
    sensor.release_interrupts()                                 # Clear interrupts

def determine_int_pin(sensor):              # find int pin routing for free fall
    int_pin = 0
    if sensor.read_register(r.KMX62_INC1, 1)[0] & b.KMX62_INC1_FFI1 > 0:
        int_pin = 1
    if sensor.read_register(r.KMX62_INC2, 1)[0] & b.KMX62_INC2_FFI2 > 0:
        int_pin = 2
    return int_pin

def determine_ff_status(data):
    channel, ins1, ins2, ins3, int_rel, na1 = data    
    print 'FREE FALL streaming mode: ', ins1 & b.KMX62_INS1_FFI > 0
    time.sleep(0.3)
    return True  # Continue reading

def read_with_stream(sensor, loop):
    # Note : pin_index = 0 == int_pin = 1
    stream = kmx62_ff_stream(sensor, pin_index=0) # FIXME! pin_index as parameter
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
                ffs_event = sensor.read_register(r.KMX62_INS1)[0] & b.KMX62_INS1_FFI  > 0

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
    sensor=kmx62_driver()
    bus = open_bus_or_exit(sensor)
    
    enable_freefall(sensor,
                    cfg=Parameter_set_1,
                    int_pin = 1)     

    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    disable_freefall(sensor)
    sensor.set_power_off()          
    bus.close()  
        
if __name__ == '__main__':
    app_main()

    