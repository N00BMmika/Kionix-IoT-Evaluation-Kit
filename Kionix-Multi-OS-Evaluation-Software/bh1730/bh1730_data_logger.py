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
from kmx62 import kmx62_data_logger, kmx62_driver
from kmx62.kmx62_driver import r as kmx62_reg
from lib.data_stream import stream_config, start_time_str, end_time_str

class bh1730_data_stream(stream_config):
    def __init__(self, sensor, sensor_kmx62):
        stream_config.__init__(self)
        # TODO make this dictionary
        assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','Only Int1 supported.'
        pin_index = 0

        self.define_request_message(sensor,
                                    fmt = "<BHHB",
                                    hdr = "ch!Als0!Als1!Int",
                                    reg = [sensor.address(), r.BH1730_DATA0LOW, 4,
                                           sensor_kmx62.address(), kmx62_reg.KMX62_INS1, 1],
                                    pin_index=pin_index)


#Integration time is IT =(256-ITIME)*2,7m. ODR = 1000/(IT +2ms). Default 218 => 1000/((256-218)*2,7) = 9,56Hz
def enable_data_logging(sensor, odr=218):     
    logger.debug('enable_data_logging start')

    if evkit_config.get('generic','int1_active_high') == 'TRUE' or evkit_config.get('generic','int2_active_high')  == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    sensor.set_power_on()
    sensor.start_measurement()

    ## select ODR
    sensor.set_odr(odr)                 # odr setting for basic data logging.

    ## Select adc gain
    sensor.set_gain(b.BH1730_GAIN_GAIN_X1_GAIN)
    # sensor.set_gain(b.BH1730_GAIN_GAIN_X2_GAIN)
    # sensor.set_gain(b.BH1730_GAIN_GAIN_X64_GAIN)
    # sensor.set_gain(b.BH1730_GAIN_GAIN_X128_GAIN)
    
    
    
    ## interrupts settings
    
    sensor.write_interrupt_thresholds(1, 0)      # always interrupt, kind of DRDY mode
    
    sensor.set_interrupt_persistence(b.BH1730_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT)
    
    ## select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_int_pin()     # interrupt 1 set        
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':   
        sensor.enable_int_pin()           
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        #sensor.disable_int_pin()
        sensor.enable_int_pin()

    sensor.start_measurement()
    
    #sensor.register_dump()
    
    logger.debug('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()
    
    # print log header
    print DELIMITER.join(['#timestamp', '10', 'Als0', 'Als1'])
    
    try:
        while count < loop or loop is None:
            count += 1
            
            sensor.drdy_function()
            sensor.clear_interrupt()
            now = timing.time_elapsed()
            c0,c1 = sensor.read_data()
            
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [c0, c1])
 
    except KeyboardInterrupt:
        print end_time_str()

    
def read_with_stream(sensor, sensor_kmx62, loop):
    stream = bh1730_data_stream(sensor, sensor_kmx62)
    kmx62_data_logger.enable_data_logging(sensor_kmx62, odr='12p5', int_number=1)
    stream.read_data_stream(sensor, sensor_kmx62, loop)
    return stream

if __name__ == '__main__':
    sensor = bh1730_driver()
       
    bus = open_bus_or_exit(sensor)
    
    enable_data_logging(sensor)

    timing.reset()
    if args.stream_mode:
        if stream_config_check() is True:
            sensor_kmx62 = kmx62_driver.kmx62_driver()
            bus.probe_sensor(sensor_kmx62)
            read_with_stream(sensor, sensor_kmx62, args.loop)
            sensor_kmx62.set_power_off()
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    
    bus.close()
