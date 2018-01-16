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

class bh1790_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self, sensor)
        # TODO make this dictionary
        assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','Only Int1 supported.'
        pin_index = 0

        self.define_request_message(\
                                    fmt = "<BHHB",
                                    hdr = "ch!Led_On!Led_Off!Int",
                                    reg = [sensor.address(), r.BH1790_DATAOUT_LEDOFF_L, 4,
                                           sensor_kmx62.address(), kmx62_reg.KMX62_INS1, 1],
                                    pin_index=pin_index)


#odr options are '64Hz' and '32Hz'
def enable_data_logging(sensor, odr='64Hz'):     
    logger.debug('enable_data_logging start')

    assert evkit_config.get('generic', 'drdy_operation') != 'DRDY_REG_POLL','Register polling not supported.'

    if evkit_config.get('generic','int1_active_high') == 'TRUE' or evkit_config.get('generic','int2_active_high')  == 'TRUE':
        logger.warning('Active high interrupt not supported. Using active low interrupt.')

    sensor.set_power_on()

    sensor.set_led_freq_128hz()
    
    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.BH1790_MEAS_CONTROL1_RCYCLE[odr])

    ## set led modes
    sensor.set_led_pulsed(led=1)
    #sensor.set_led_constant(led=1)
    sensor.set_led_pulsed(led=2)
    #sensor.set_led_constant(led=2)
    
    sensor.set_led_on_time_216us()
    #sensor.set_led_on_time_216us()
    
    sensor.set_led_current(b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA)
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA
    #b.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA
    
    
    ## select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        print "BH1790 does not support interrupt pin. Use additional sensor to support drdy"
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':   
        print "BH1790 does not support interrupt pin. Use additional sensor to support drdy"

    sensor.start_measurement()
    
    #sensor.register_dump()
    
    logger.debug('enable_data_logging done')

def read_with_polling(sensor, sensor_kmx62, loop):
    count = 0

    print start_time_str()
    
    # print log header
    print DELIMITER.join(['#timestamp','10','Led_On','Led_Off'])
    
    try:
        while count < loop or loop is None:
            count += 1

            if (sensor_kmx62):
                sensor_kmx62.drdy_function()
                sensor_kmx62.release_interrupts()
            else:
                sensor.drdy_function()
            now = timing.time_elapsed()
            c0,c1 = sensor.read_data()
            
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [c0,c1])
 
    except KeyboardInterrupt:
        print end_time_str()

    
def read_with_stream(sensor, loop):
    stream = bh1790_data_stream(sensor)
    kmx62_data_logger.enable_data_logging(sensor_kmx62, odr=25, int_number = 1)
    stream.read_data_stream(loop)
    return stream

if __name__ == '__main__':
    sensor = bh1790_driver()
    bus = open_bus_or_exit(sensor)  
    enable_data_logging(sensor)
    sensor_kmx62 = None

    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor_kmx62 = kmx62_driver.kmx62_driver()
        bus.probe_sensor(sensor_kmx62)
        kmx62_data_logger.enable_data_logging(sensor_kmx62, odr='12p5', int_number = 1)
        
    timing.reset()
    if args.stream_mode:
        if stream_config_check() is True:
            print "\nBH1790 does not support interrupt pin. Using KMX62 to get drdy.\n"
            read_with_stream(sensor, args.loop)
            sensor_kmx62.set_power_off()
        else:
            logger.error(stream_config_check())
    else:
        read_with_polling(sensor, sensor_kmx62, args.loop)

    sensor.set_power_off()

    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor_kmx62.set_power_off()
    
    bus.close()
