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
magnetic field wakeup detection

INT1 pin is used for mag wu interrupt
'''
_CODE_FORMAT_VERSION = 2.0
from imports import *



## magnetic field axes which used (masked in) for detection

class Parameter_set_1:        
    KMX62_MMICT     = 0x01                      # wakeup control timer
    KMX62_MMITH     = 0x02                      # threshold for wakeup 
    LOW_POWER_MODE  = False
    odr_OSM         = 25
    lp_average      = 'A32M16'
    odr_OSA         = 25
    KMX62_MMI_AXES  =   b.KMX62_INC5_MXNIE | \
                        b.KMX62_INC5_MXPIE #| \
                        #b.KMX62_INC5_MYNIE | \
                        #b.KMX62_INC5_MYPIE | \
                        #b.KMX62_INC5_MZNIE | \
                        #b.KMX62_INC5_MZPIE     # MMI motion axes    
def enable_mag_wu(sensor,
                    cfg = Parameter_set_1,
                    power_off_on = True):
                    
    logger.info('enable_mag_wu start')
    
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
            
    assert cfg.LOW_POWER_MODE in [True,False],\
    'Invalid LOW_POWER_MODE value "{}" valid values are {}'.format(
    cfg.LOW_POWER_MODE, [True,False])           
    
    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
        
    ##Select acc ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)], CH_ACC)                  # set acc stream ODR

    ##Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[convert_to_enumkey(cfg.odr_OSM)], CH_MAG)                  # set mag stream ODR

    ## Low power mode (accelerometer and magnetometer)
    if cfg.LOW_POWER_MODE:
        sensor.set_average(e.KMX62_CNTL2_RES[cfg.lp_average], None, CH_ACC)
    ## Full power mode
    else:
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2,None, CH_ACC)
        
    ## interrupts
    sensor.set_bit(r.KMX62_INC1, b.KMX62_INC1_MMI1)         # mmi motion to int 1
    
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        IEA1 = b.KMX62_INC3_IEA1_HIGH
    else:
        IEA1 = b.KMX62_INC3_IEA1_LOW   
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        IEA2 = b.KMX62_INC3_IEA2_HIGH
    else:
        IEA2 = b.KMX62_INC3_IEA2_LOW
    sensor.write_register(r.KMX62_INC3, b.KMX62_INC3_IED2_PUSHPULL   | \
                                        IEA2                         | \
                                        b.KMX62_INC3_IEL2_LATCHED    | \
                                        b.KMX62_INC3_IED1_PUSHPULL   | \
                                        IEA1                         | \
                                        b.KMX62_INC3_IEL1_LATCHED)    # both int pins active

    ## MMI motion setup
    sensor.write_register(r.KMX62_INC5, cfg.KMX62_MMI_AXES)     # masked axes
    sensor.write_register(r.KMX62_MMI_CNTL1, cfg.KMX62_MMITH)   # motion threshold
    sensor.write_register(r.KMX62_MMI_CNTL2, cfg.KMX62_MMICT)   # motion counter
    sensor.write_register(r.KMX62_MMI_CNTL3, b.KMX62_MMI_CNTL3_MMI_EN_ENABLED |
                                             b.KMX62_MMI_CNTL3_OMMI_25) # MMI on + MMI odr
    
    ## power on sensor
    if power_off_on:
        sensor.set_power_on(CH_MAG)                             # measurement start

    #sensor.register_dump()    
    logger.info('enable_mag_wu done')
    logger.info('\nWaiting for magnetic field motion interrupt.')

    sensor.release_interrupts()                             # clear ints
    
def disable_wu_mag(sensor):
    sensor.set_bit(r.KMX62_MMI_CNTL3, b.KMX62_MMI_CNTL3_MMI_EN_DISABLED)    # mag wu disable    

def readAndPrint(sensor):
    valid_mmi = False
    pin_condition = 0
    if evkit_config.get('generic','int1_active_high')=='TRUE':
        pin_condition = 1

    while valid_mmi == False:
        if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':
            valid_mmi = sensor._bus.poll_gpio(1) == pin_condition
        else:
            valid_mmi = sensor.read_register(r.KMX62_INS1)[0] & b.KMX62_INS1_MMI_MOTION > 0

        if valid_mmi:
            print 'MMI MOTION WAKEUP DETECTION: MOVING, axes','{:08b}'.format(sensor.read_register(r.KMX62_INS3)[0])
            time.sleep(0.1)
            sensor.release_interrupts()

def read_with_polling(sensor):
    try:        
        while 1:
            readAndPrint(sensor)
          
    except KeyboardInterrupt:
        pass      
def app_main():
    sensor=kmx62_driver()
    bus = open_bus_or_exit(sensor)

    try:
        enable_mag_wu(sensor)
        read_with_polling(sensor)
            
    finally:
        disable_wu_mag(sensor)        
        sensor.set_power_off()
        bus.close()  
if __name__ == '__main__':
    app_main()

    