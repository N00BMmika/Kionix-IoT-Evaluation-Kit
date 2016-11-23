# The MIT License (MIT)
#
# Copyright 2016 Kionix Inc.
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

def init_data_logging(sensor):
    logger.debug('init_data_logging start')
    sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings
    ## set odr
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_0P781)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_1P563)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_3P125)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_6P25)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_12P5)
    sensor.set_odr(b.KXCNL_CNTL1_ODR_25)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_50)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_100)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_400)
    #sensor.set_odr(b.KXCNL_CNTL1_ODR_1600)

    ## set range
    sensor.set_range(b.KXCNL_CNTL1_SC_2G)
    #sensor.set_range(b.KXCNL_CNTL1_SC_4G)
    #sensor.set_range(b.KXCNL_CNTL1_SC_6G)
    #sensor.set_range(b.KXCNL_CNTL1_SC_8G)

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

    sensor.set_power_on()
    logger.debug('init_data_logging done')

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
if __name__ == '__main__':
    sensor = kxcnl_driver()
    bus = open_bus_or_exit(sensor)
    init_data_logging(sensor)
    timing.reset()
    assert args.stream_mode == False, 'Streaming not implemented yet'
    read_with_polling(sensor, args.loop)
    sensor.set_power_off()
    bus.close()
