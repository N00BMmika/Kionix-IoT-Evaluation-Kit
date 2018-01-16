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
FIFO test
    test application with watermark level detection
    INT1 pin is used for watermark interrupt
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *
               
class Parameter_set_1:
    """Basic FIFO settings"""
    odr_OSA         = 25
    odr_OSM         = 25
    LOW_POWER_MODE  = False
    lp_average      = 'A32M16'
    acc_range       = '2G'

def enable_fifo(sensor,
                cfg = Parameter_set_1,
                buffered_axes = \
                                   b.KMX62_BUF_CTRL_3_BUF_AX_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_AY_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_AZ_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_MX_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_MY_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_MZ_ENABLED | \
                                   b.KMX62_BUF_CTRL_3_BUF_TEMP_ENABLED,
                samples_to_buffer = 10,
                power_off_on = True):
                
    logger.info('enable_fifo start')
    
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
    
    all_axes_mask = (b.KMX62_BUF_CTRL_3_BUF_AX_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_AY_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_AZ_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_MX_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_MY_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_MZ_ENABLED | \
                        b.KMX62_BUF_CTRL_3_BUF_TEMP_ENABLED)
    
    assert buffered_axes & ~all_axes_mask == 0,\
    'Invalid buffered_axes value'              
    
    AXES = bin(buffered_axes).count('1')        # finding buffered axes count
    assert AXES > 0, 'Atleast 1 buffered_axes must be given and no more than 7'
    
    buffer_full = int(3072 / (AXES * 2))        # max samples in buffer
    watermark = samples_to_buffer * AXES * 2    # databytes in buffer before watermark event
    assert(watermark <= buffer_full),\
    "Value samples_to_buffer = {} too high for {} axes".format(
    samples_to_buffer, AXES)  
    
   
    
    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
        
    #
    # Configure sensor
    #
        
    ##Select acc ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)], CH_ACC) 
    
    ##Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[convert_to_enumkey(cfg.odr_OSM)], CH_MAG)     #mag odr

    ## select g-range (for acc)
    sensor.set_range(e.KMX62_CNTL2_GSEL[cfg.acc_range], None, CH_ACC)
  

    #power mode (accelerometer and magnetometer)
    if cfg.LOW_POWER_MODE:
        # Low power mode
        sensor.set_average(e.KMX62_CNTL2_RES[cfg.lp_average], None, CH_ACC)
    else:
        # Full power mode
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2,None, CH_ACC)

    ## buffer controls
    sensor.enable_fifo(b.KMX62_BUF_CTRL_2_BUF_M_STREAM,16, buffered_axes)     # stream mode, buffer input mask (acc + mag)
    ## select watermark level
    sensor.set_fifo_watermark_level(watermark)              # 
    
    ## interrupts
    sensor.set_bit(r.KMX62_INC1, b.KMX62_INC1_WMI1)         # water mark to int 1
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
                                        
    #
    # Turn on operating mode (disables setup)
    #
    ## power on sensor(s)
    # NOTE FIFO does not work if temp is not enabled
    if power_off_on:
        sensor.set_power_on(CH_ACC | CH_MAG | CH_TEMP)          # also tempsensor because fifo actions
                            
    #sensor.register_dump();#sys.exit()

    logger.info('enable_fifo done')

    sensor.release_interrupts() # clear ints, just in case

def readAndPrint(sensor):   
    valid_wmi = False
    pin_condition = 0
    if evkit_config.get('generic','int1_active_high')=='TRUE':
        pin_condition = 1

    ## HOX! buffer clear function must closely proceed just before first interrupt signal follow-up
    ## please ensure that maximum time after clear_buffer to first interrupt detection
    ## in less than "1/ODR*watermark"
    sensor.clear_buffer()
    #read axis count
    AXES = bin(sensor.read_register(r.KMX62_BUF_CTRL_3)[0] & 0x7f).count('1')   
    while valid_wmi == False:
        if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':
            status = sensor._bus.poll_gpio(1)
            if status == pin_condition:
                valid_wmi = True
        else:
            valid_wmi = sensor.read_register(r.KMX62_INS1)[0] & b.KMX62_INS1_WMI_MARK_REACHED > 0
            
        if valid_wmi == True:
            logger.debug('Watermark occured')
            ## fetch data from buffer and print status
            bytes_in_buffer = sensor.get_fifo_level()  
            # buf_storage = sensor.read_register(r.KMX62_BUF_READ,)
            now_ms = int(time.clock() * 1000)
            samples_in_buffer = bytes_in_buffer / (AXES * 2)
            print 'time %d, samples got %d / %d' % (now_ms, (samples_in_buffer ), bytes_in_buffer / (AXES*2))
            logger.debug('Waiting new watermark event')
                    
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
        enable_fifo(sensor)
        read_with_polling(sensor)
        
    finally:
        sensor.clear_buffer()
        sensor.disable_fifo()
        sensor.set_power_off()          
        bus.close()    
        
if __name__ == '__main__':
    app_main()
