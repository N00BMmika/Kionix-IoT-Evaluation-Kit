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

class bm1383aglv_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)
        assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','Only Int1 supported.'
        pin_index = 0

        self.define_request_message(sensor,
                                    fmt = ">BBHBh",
                                    hdr = "ch!stat!P_raw!P_raw_xlb!T_raw",
                                    reg = r.BM1383AGLV_STATUS_REG,
                                    pin_index=pin_index)

def enable_data_logging(sensor, odr='avg_16_50ms'):
    logger.debug('enable_data_logging start')

    if evkit_config.get('generic','int1_active_high') == 'TRUE' or evkit_config.get('generic','int2_active_high')  == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    sensor.set_power_on()

    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM[odr])                 # odr setting for basic data logging

    ## Select averaging time / ODR
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS)    # meastime 3ms, interval 50ms (ODR 20)
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS)   # meastime 5ms, interval 50ms
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS)    # meastime 10ms, interval 50ms
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS)   # meastime 19ms, interval 50ms
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS)  # meastime 37ms, interval 50ms
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS)  # meastime 74ms, interval 100ms  (ODR 10)
    #sensor.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS)  # meastime 147ms, interval 200ms (ODR 5)
    
    
    ## interrupts settings
    ## select dataready routing for sensor = int1 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy_pin()                  
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.disable_drdy_pin()

    sensor.start_continuous_measurement()
    
    #sensor.register_dump()
    
    logger.debug('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header
    print DELIMITER.join(['#timestamp','10','Temperature','Pressure'])
    
    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            sensor.reset_drdy_pin()
            now = timing.time_elapsed()
            c0,c1 = sensor.read_temperature_pressure()
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:f}'.format(t) for t in [c0, c1])

    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    stream = bm1383aglv_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream

if __name__ == '__main__':
    sensor = bm1383aglv_driver()
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
