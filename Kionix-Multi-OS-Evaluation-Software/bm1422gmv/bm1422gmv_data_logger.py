# The MIT License (MIT)
#
# Copyright (c) 2016 Rohm Semiconductor
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
## basic logger application
###
## logging polling or stream
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class bm1422gmv_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)
        assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','Only Int1 supported.'
        pin_index = 0

        self.define_request_message(sensor,
                                    fmt = "<Bhhh",
                                    hdr = "ch!mx!my!mz",
                                    reg = r.BM1422GMV_DATAX,
                                    pin_index=pin_index)

def enable_data_logging(sensor, odr='20'):
    logger.debug('enable_data_logging start')

    if evkit_config.get('generic','int1_active_high') == 'TRUE' or evkit_config.get('generic','int2_active_high')  == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    sensor.set_power_on()

    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.BM1422GMV_CNTL1_ODR[odr])                 # odr setting for basic data logging

    ## Select averaging time / ODR
    #sensor.set_averaging(b.BM1422GMV_AVER_AVG_1TIMES)
    #sensor.set_averaging(b.BM1422GMV_AVER_AVG_2TIMES)
    sensor.set_averaging(b.BM1422GMV_AVER_AVG_4TIMES)
    #sensor.set_averaging(b.BM1422GMV_AVER_AVG_8TIMES)
    #sensor.set_averaging(b.BM1422GMV_AVER_AVG_16TIMES)
    
    
    
    ## interrupts settings

    sensor.set_drdy_low_active()
    
    ## select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy_pin()     # interrupt 1 set        
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':   
        sensor.enable_drdy_pin()           
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.disable_drdy_pin()                      # drdy must be enabled also when register polling  ?????

    #sensor.set_power_on()
    sensor.start_continuous_measurement()

    
    
    #sensor.register_dump()
    
    logger.debug('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header
    print DELIMITER.join(['#timestamp','10','mx','my','mz', 'temp'])
    
    try:
        while count < loop or loop is None:
            count += 1
            
            sensor.drdy_function()
            #sensor.reset_drdy_pin()
            now = timing.time_elapsed()
            temp,mx,my,mz = sensor.read_data_raw()
            
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [mx, my, mz,temp])

    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    stream = bm1422gmv_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream

if __name__ == '__main__':
    sensor = bm1422gmv_driver()
    bus = open_bus_or_exit(sensor)
    
    enable_data_logging(sensor)

    timing.reset()
    if args.stream_mode:
        if stream_config_check() is True:            
            read_with_stream(sensor, args.loop)
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()
