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
## basic logger application
###
## logging polling or stream
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class kxtj3_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)
        # TODO make this dictionary
        pin_index = 0

        self.define_request_message(sensor,
                                    fmt = "<Bhhh",
                                    hdr = "ch!ax!ay!az",
                                    reg = r.KXTJ3_XOUT_L,
                                    pin_index=pin_index)

def enable_data_logging(sensor, odr = 25, acc_fs = '2G', lp_mode=False):
    assert acc_fs in ['2G', '16G',  '4G',   '16G2',
                      '8G', '16G3', '8G_14','16G_14'], 'Invalid value for acc_fs'

    logger.debug('init_data_logging start')
    sensor.set_power_off()
    
    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.KXTJ3_DATA_CTRL_REG_OSA[odr])  # odr setting for basic data logging

    ## select g-range and measurement bits
    sensor.set_range(e.KXTJ3_CTRL_REG1_GSEL[acc_fs])    
    #sensor.set_range(b.KXTJ3_CTRL_REG1_GSEL_16G_14)

    ## resolution / power mode selection
    LOW_POWER_MODE = False
    if LOW_POWER_MODE == True:
        sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)# low resolution mode           
    else:
        sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)# high resolution mode
     
    ## interrupts settings
    ## select dataready routing for sensor = int1 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy()
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)    # enable interrupt pin        
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy()                # drdy must be enabled also when register polling
    ## interrupt signal parameters
    sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEL)  # latched interrupt
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEA) # active high
    else:
        sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEA)# active low

    sensor.set_power_on()
    
    #sensor.register_dump()#;sys.exit()

    logger.debug('init_data_logging done')
    
    sensor.release_interrupts()
    
def read_with_polling(sensor, loop):
    ## HOX! data is in raw 16b mode 
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
            
            #sensor.release_interrupts()

    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    ## HOX! data is in raw 16b mode
    stream = kxtj3_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream

if __name__ == '__main__':
    sensor=kxtj3_driver()
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
