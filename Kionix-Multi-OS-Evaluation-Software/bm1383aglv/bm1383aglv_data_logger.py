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
"""
BM1383AGLV data logger application
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *

class bm1383aglv_data_stream(stream_config):

    def __init__(self, sensor, pin_index = None):
        stream_config.__init__(self, sensor)
        
        if pin_index is None:
            pin_index=0

        assert pin_index in [0], 'Sensor can only be connected to adapter logical int pin 0'
            
        self.define_request_message(\
            fmt = ">BBHBh",
            hdr = "ch!stat!P_raw!P_raw_xlb!T_raw",
            reg = r.BM1383AGLV_STATUS_REG,
            pin_index=pin_index)

def enable_data_logging(sensor, odr='AVG_16_50MS'):
    logger.info('enable_data_logging start')

    #
    # parameter validation
    #
    if evkit_config.get('generic','int1_active_high') == 'TRUE' or evkit_config.get('generic','int2_active_high')  == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    sensor.set_power_on()

    #
    # Configure sensor
    #
    
    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM[odr])                 # odr setting for basic data logging

    
    #
    ## interrupts settings
    #

    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy_pin()                  
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.disable_drdy_pin()

    #
    # Turn on measurement
    #

    sensor.start_continuous_measurement()
    
    #sensor.register_dump()#;sys.exit()
    
    logger.debug('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0
    timing.reset()
    print (start_time_str())

    # print log header. 10 is channel number
    print (DELIMITER.join(['#timestamp','10','Temperature','Pressure']))

    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            sensor.reset_drdy_pin()
            now = timing.time_elapsed()
            c0,c1 = sensor.read_temperature_pressure()
            print ('{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:f}'.format(t) for t in [c0, c1]))

    except (KeyboardInterrupt):
        print (end_time_str())

def read_with_stream(sensor, loop):
    stream = bm1383aglv_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream


def app_main(odr = 'AVG_16_50MS'):
    sensor = bm1383aglv_driver()
    bus = open_bus_or_exit(sensor)
    enable_data_logging(sensor, odr = odr)

    if args.stream_mode:
        if stream_config_check() is True:            
            read_with_stream(sensor, args.loop)
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()


if __name__ == '__main__':
    app_main()
