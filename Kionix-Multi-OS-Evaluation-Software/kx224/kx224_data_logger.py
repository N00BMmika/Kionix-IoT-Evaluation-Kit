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
## basic logger application for KX224
###
## logging polling or stream
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class kx224_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)
        # TODO make this dictionary
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            pin_index = 0
        else:
            pin_index = 1

        self.define_request_message(sensor,
                                    fmt = "<Bhhh",
                                    hdr = "ch!ax!ay!az",
                                    reg = r.KX224_XOUT_L,
                                    pin_index=pin_index)

def enable_data_logging(sensor, odr=25, acc_fs = '8g', lp_mode=False):
    assert acc_fs in [ '8g','16g','32g'], 'Invalid value for acc_fs'

    assert lp_mode in [
        False,
        'NO_AVG',
        '2_SAMPLE_AVG',
        '4_SAMPLE_AVG',
        '8_SAMPLE_AVG',
        '16_SAMPLE_AVG',
        '32_SAMPLE_AVG',
        '64_SAMPLE_AVG',
        '128_SAMPLE_AVG',
        ], 'Invalid value for lp_mode'

    logger.debug('enable_data_logging start')
    sensor.set_power_off()                                  # this sensor request PC=0 to PC=1 before valid settings

    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.KX224_ODCNTL_OSA[odr])                 # odr setting for basic data logging
    
    ## select g-range
    sensor.set_range(e.KX224_CNTL1_GSEL[acc_fs])    
    #sensor.set_range(b.KX224_CNTL1_GSEL_8G)

    ## resolution / power mode selection
    ## Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)

    if lp_mode != False:
        sensor.reset_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)  # low current
        sensor.set_average(e.KX224_LP_CNTL_AVC[lp_mode])
    else:
        sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)    # high resolution

    ## set bandwitdh
    #sensor.set_BW(b.KX224_ODCNTL_LPRO, 0, CH_ACC)           # odr / 2
    sensor.set_BW(0, 0, CH_ACC)                             # odr / 9
    
    ## interrupts settings
    ## select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(intpin = 1)
        sensor.set_bit(r.KX224_INC1, b.KX224_INC1_IEN1)     # interrupt 1 set        
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':   
        sensor.enable_drdy(intpin = 2)
        sensor.set_bit(r.KX224_INC5, b.KX224_INC5_IEN2)     # interrupt 2 set           
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy(intpin = 1)                      # drdy must be enabled also when register polling
    ## interrupt signal parameters
    sensor.reset_bit(r.KX224_INC1, b.KX224_INC1_IEL1)       # latched interrupt int1
    sensor.reset_bit(r.KX224_INC5, b.KX224_INC5_IEL2)       # latched interrupt int2
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KX224_INC1, b.KX224_INC1_IEA1)     # active high
    else:
        sensor.reset_bit(r.KX224_INC1, b.KX224_INC1_IEA1)   # active low
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        sensor.set_bit(r.KX224_INC5, b.KX224_INC5_IEA2)     # active high
    else:
        sensor.reset_bit(r.KX224_INC5, b.KX224_INC5_IEA2)   # active low

    sensor.set_power_on()                                   # settings coming to valid and start measurements
    
    #sensor.register_dump()
    
    logger.debug('enable_data_logging done')
    
def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header. 10 is channel number
    print DELIMITER.join(['#timestamp','10','ax','ay','az'])

    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            ax, ay, az = sensor.read_data()
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [ax, ay, az])

    except KeyboardInterrupt:
        print end_time_str()       

def read_with_stream(sensor, loop):
    stream = kx224_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream

if __name__ == '__main__':
    sensor = kx224_driver()
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
