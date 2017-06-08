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
## KMX62 logger application
##
###

from imports import *
from lib.data_stream import stream_config, start_time_str, end_time_str

class kmx62_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)
        assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','This example for KMX62 supports only int1 on iot node'
        self.define_request_message(sensor,
                                    fmt = "<Bhhhhhh",
                                    hdr = "ch!ax!ay!az!mx!my!mz",
                                    reg = r.KMX62_ACCEL_XOUT_L,
                                    pin_index=0)
    
def enable_data_logging(sensor, odr = 25, int_number = None):
    """ Configure sensor for data reading
    
    pin_index = None means use pin definition in settings.cfg"""
    assert int_number in [None,1,2] # Note Kionix IoT Node has only kmx62 int1 connected
    
    logger.debug('enable_data_logging start')
    
    sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings
    # Select acc ODRs
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.KMX62_ODCNTL_OSA[odr], CH_ACC)                   # set ODR

    # Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[odr], CH_MAG)                   # set ODR
    
    # select g-range (for acc)
    sensor.set_range(b.KMX62_CNTL2_GSEL_2G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_4G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_8G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_16G, C_ACC)
    
    ## power mode (accelerometer and magnetometer)
    LOW_POWER_MODE = False
    if LOW_POWER_MODE == True:
        sensor.set_average(b.KMX62_CNTL2_RES_A4M2, None, CH_ACC)
        sensor.set_average(b.KMX62_CNTL2_RES_A32M16, None, CH_ACC)
    else:
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2,None, CH_ACC)

    ## interrupt settings            
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        IEA1 = b.KMX62_INC3_IEA1_HIGH
    else:
        IEA1 = b.KMX62_INC3_IEA1_LOW    
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        IEA2 = b.KMX62_INC3_IEA2_HIGH
    else:
        IEA2 = b.KMX62_INC3_IEA2_LOW

    
    if int_number is None:
        ## KMX62: interrupt source selection activates also physical interrupt pin    
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            sensor.enable_drdy(1, CH_ACC)                       # acc data ready to int1
            #sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
        elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
            sensor.enable_drdy(2, CH_ACC)                       # acc data ready to int2
            #sensor.enable_drdy(2, CH_MAG)                       # mag data ready to int2        
        elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
            sensor.enable_drdy(1, CH_ACC)                       # acc data ready to int1
            #sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
    else:
        sensor.enable_drdy(int_number, CH_ACC)
        
    ## interrupt signal parameters
    # TODO replace with write_register since whole byte is written
    sensor.set_bit_pattern(r.KMX62_INC3, b.KMX62_INC3_IEL1_LATCHED   |  \
                                         IEA1                        |  \
                                         b.KMX62_INC3_IED1_PUSHPULL  |  \
                                         b.KMX62_INC3_IEL2_LATCHED   |  \
                                         IEA2                        |  \
                                         b.KMX62_INC3_IED2_PUSHPULL,    \
                                         0xff)

    ## start measurement
    #sensor.set_power_on(CH_MAG )                       # mag ON
    #sensor.set_power_on(CH_ACC | CH_MAG )              # acc + mag ON
    sensor.set_power_on(CH_ACC | CH_MAG | CH_TEMP)     # acc + mag + temp ON

    #sensor.register_dump()#;sys.exit()
    
    sensor.read_data()                              # this latches data ready interrupt register and signal
    
    sensor.release_interrupts()                     # clear all internal function interrupts

    logger.debug('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0

    print start_time_str()

    # print log header
    print DELIMITER.join(['#timestamp','10','ax','ay','az','mx','my','mz'])
    
    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()
            now = timing.time_elapsed()
            ax, ay, az, mx, my, mz = sensor.read_data()
            print '{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in [ax, ay, az, mx, my, mz])

    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    stream = kmx62_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    return stream

if __name__ == '__main__':
    sensor = kmx62_driver()
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
