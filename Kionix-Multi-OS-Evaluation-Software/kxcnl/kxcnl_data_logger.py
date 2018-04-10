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
from imports import *

_CODE_FORMAT_VERSION = 2.0

def enable_data_logging(sensor,
                        odr = 25,
                        max_range = '2G',
                        power_off_on = True):
    logger.info('enable_data_logging start')
    #
    # parameter validations
    #
    
    assert convert_to_enumkey(odr) in e.KXCNL_CNTL1_ODR.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    odr,e.KXCNL_CNTL1_ODR.keys())
    
    assert max_range in e.KXCNL_CNTL1_SC.keys(),\
    'Invalid max_range value "{}". Valid values are {}'.format(
    max_range,e.KXCNL_CNTL1_SC.keys())
    
    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings
    #  
    # Configure sensor  
    #    
    ## set odr
    sensor.set_odr(e.KXCNL_CNTL1_ODR[convert_to_enumkey(odr)])

    ## set range
    sensor.set_range(e.KXCNL_CNTL1_SC[max_range])


    ## interrupts settings
    ## KXCNL not dataready not true latch capable, any polling of signal or register not possible
    assert evkit_config.get('generic','drdy_operation') == 'INTERVAL_READ', 'Only "INTERVAL_READ" drdy_operation supported. Now "%s" is selected.' % evkit_config.get('generic','drdy_operation')

    ## this sensor has same setups for both physical interrupt signals
    sensor.set_bit(r.KXCNL_CNTL1, b.KXCNL_CNTL1_IEN)    # physical interrupts enabled
    assert evkit_config.get('generic','int1_active_high') == evkit_config.get('generic','int2_active_high'), \
           'Sensor requres same polarity on both interrupt lines.'
    ## interrupt signal parameters
    sensor.reset_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_IEL)  # latched interrupt

    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_IEA) # active high
    else:
        sensor.reset_bit(r.KXCNL_CNTL4, b.KXCNL_CNTL4_IEA)# active low

    # sensor.register_dump()

    #
    #Turn on operating mode (disables setup)
    #
    if power_off_on:
        sensor.set_power_on()
        
    logger.info('init_data_logging done')

def readAndPrint(sensor):
    sensor.drdy_function()
    now = timing.time_elapsed()
    x,y,z = sensor.read_data()
    print '%f%s%d%s%d%s%d%s' % (now, DELIMITER, \
                            x, DELIMITER, \
                            y, DELIMITER, \
                            z, DELIMITER)

def read_with_polling(sensor, loop):
    try:
        if loop == None:
            while 1:
                readAndPrint(sensor)
        else:
            for i in range (loop):
                readAndPrint(sensor)
    except(KeyboardInterrupt):
        pass
    finally:
        sensor.set_power_off()
        
def app_main():
    sensor = kxcnl_driver()
    bus = open_bus_or_exit(sensor)
    enable_data_logging(sensor)
    timing.reset()
    args = get_datalogger_args()  
    assert args.stream_mode == False, 'Streaming not implemented yet'
    read_with_polling(sensor, args.loop)
    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()