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
"""
KXG08 data logger application
"""

_CODE_FORMAT_VERSION = 2.0
from imports import *

class kxg08_data_stream(stream_config):
    
    def __init__(self, sensor, pin_index = None):
        stream_config.__init__(self, sensor)

        if pin_index is None:
            pin_index=get_pin_index()
            
        # Default way to define request message
        self.define_request_message(fmt = "<Bhhhhhhh",
                                    hdr = "ch!temperature!gx!gy!gz!ax!ay!az",
                                    reg = r.KXG08_TEMP_OUT_L,
                                    pin_index=pin_index)
        
        # Advanced way to define request message
##        self.define_request_message(\
##                                    fmt = "<Bhhhhhh"+ext.fmt_packet_count_8,
##                                    hdr = "ch!gx!gy!gz!ax!ay!az"+ext.hdr_packet_count_8,
##                                    reg = [sensor.address(), r.KXG08_XOUT_L, 12] + ext.reg_packet_count_8,
##                                    pin_index=pin_index)

def enable_data_logging(sensor,
                        odr = 25,
                        max_range = '2G',                        
                        odr_acc = None,
                        odr_gyro = None,
                        max_range_acc = None,
                        max_range_gyro = None,
                        lp_mode = False,
                        lp_mode_acc = None,
                        lp_mode_gyro = None,
                        power_off_on = True       # set to False if this function is part of other configuration
                        ):
                        
    logger.info('enable_data_logging start')


    #
    # parameter validation
    #
    ## key validation    
    assert convert_to_enumkey(odr) in e.KXG08_ACCEL_ODR_ODRA.keys(), \
    'Invalid odr value "{}". Valid values are {}'.format(
    odr,e.KXG08_ACCEL_ODR_ODRA.keys())
    
    if odr_acc != None:
        assert convert_to_enumkey(odr_acc) in e.KXG08_ACCEL_ODR_ODRA.keys(), \
        'Invalid odr_acc value "{}". Valid values are None or {}'.format(
        odr_acc,e.KXG08_ACCEL_ODR_ODRA.keys())
        
    if odr_gyro != None:
        assert convert_to_enumkey(odr_gyro) in e.KXG08_GYRO_ODR_ODRG.keys(), \
        'Invalid odr_gyro value "{}". Valid values are None or {}'.format(
        odr_gyro,e.KXG08_GYRO_ODR_ODRG.keys()) 

    assert max_range in e.KXG08_ACCEL_CTL_ACC_FS.keys(), \
    'Invalid max_range value "{}". Valid values are {}'.format(
    max_range,e.KXG08_ACCEL_CTL_ACC_FS.keys())
    
    assert max_range_acc in e.KXG08_ACCEL_CTL_ACC_FS or max_range_acc == None, \
    'Invalid max_range_acc value "{}". Valid values are None or {}'.format(
    max_range_acc,e.KXG08_ACCEL_CTL_ACC_FS.keys())
    
    assert max_range_gyro in e.KXG08_GYRO_CTL_GYRO_FS or max_range_gyro == None, \
    'Invalid max_range_acc value "{}". Valid values are None or {}'.format(
    max_range_gyro,e.KXG08_GYRO_CTL_GYRO_FS.keys())

    assert lp_mode in e.KXG08_ACCEL_ODR_NAVGA.keys() or lp_mode == False, \
    'Invalid lp_mode value "{}". Valid values are False or {}'.format(
    lp_mode,e.KXG08_ACCEL_ODR_NAVGA.keys())
        
    assert lp_mode_acc in e.KXG08_ACCEL_ODR_NAVGA.keys() or lp_mode_acc == None, \
    'Invalid lp_mode_acc value "{}". Valid values are None or {}'.format(
    lp_mode_acc,e.KXG08_ACCEL_ODR_NAVGA.keys())
    
    assert lp_mode_gyro in e.KXG08_GYRO_ODR_NAVGG.keys() or lp_mode_gyro == None, \
    'Invalid lp_mode_gyro value "{}". Valid values are None or {}'.format(
    lp_mode_gyro,e.KXG08_GYRO_ODR_NAVGG.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    ## odr setting for data logging
    if odr_acc == None:
        sensor.set_odr(e.KXG08_ACCEL_ODR_ODRA[convert_to_enumkey(odr)], CH_ACC)
    else:
        sensor.set_odr(e.KXG08_ACCEL_ODR_ODRA[convert_to_enumkey(odr_acc)], CH_ACC)
    if odr_gyro == None:
        sensor.set_odr(e.KXG08_GYRO_ODR_ODRG[convert_to_enumkey(odr)], CH_GYRO)        
    else:
        sensor.set_odr(e.KXG08_GYRO_ODR_ODRG[convert_to_enumkey(odr_gyro)], CH_GYRO)

    ## max_range settings for data logging
    if max_range_acc == None:
        sensor.set_range(e.KXG08_ACCEL_CTL_ACC_FS[convert_to_enumkey(max_range)], CH_ACC)        
    else:
        sensor.set_range(e.KXG08_ACCEL_CTL_ACC_FS[convert_to_enumkey(max_range_acc)], CH_ACC)
    if max_range_gyro != None:
        sensor.set_range(e.KXG08_GYRO_CTL_GYRO_FS[convert_to_enumkey(max_range_gyro)], CH_GYRO)

    ## resolution and power modes for data logging
    ### a lot of magic
    if lp_mode_acc == None and lp_mode == False:                  # power mode for acc
        sensor.set_average(False, channel=CH_ACC)
    elif lp_mode_acc == None and lp_mode != False:
        sensor.set_average(e.KXG08_ACCEL_ODR_NAVGA[convert_to_enumkey(lp_mode)],
                           channel=CH_ACC)                
    elif lp_mode_acc != None:
        sensor.set_average(e.KXG08_ACCEL_ODR_NAVGA[convert_to_enumkey(lp_mode_acc)], \
                           channel=CH_ACC)
        
    if lp_mode_gyro == None and lp_mode == False:                  # power mode for gyro
        sensor.set_average(False, channel=CH_GYRO)
    elif lp_mode_gyro == None and lp_mode != False:
        sensor.set_average(e.KXG08_GYRO_ODR_NAVGG[convert_to_enumkey(lp_mode)],
                           channel=CH_GYRO)                
    elif lp_mode_gyro != None:
        sensor.set_average(e.KXG08_GYRO_ODR_NAVGG[convert_to_enumkey(lp_mode_gyro)], \
                           channel=CH_GYRO)
 
    ## bandwidth
    #sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, CH_ACC)       # bandwidth acc      
    sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_8, CH_ACC)       # bandwidth acc 
    #sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, CH_GYRO)      # bandwidth gyro
    sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_8, CH_GYRO)      # bandwidth gyro

    #
    # interrupts pin routings and settings
    #
    
    ## select dataready routing for sensor = int1, int2 or register polling 
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(1, CH_ACC)                                   # acc data ready to int1
        #sensor.enable_drdy(1, CH_GYRO)                                 # gyro data ready to int1
        sensor.set_bit(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEN1)
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':
        sensor.enable_drdy(2, CH_ACC)                                   # acc data ready to int2
        #sensor.enable_drdy(2, CH_GYRO)                                 # gyro data ready to int2
        sensor.set_bit(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEN2)        
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when polling
        sensor.enable_drdy(1, CH_ACC)
        
    ## interrupt signal parameters
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)        
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW)          
    sensor.set_bit_pattern(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEL2_LATCHED | \
                                                b.KXG08_INT_PIN_CTL_IEL1_LATCHED, \
                                                m.KXG08_INT_PIN_CTL_IEL2_MASK | \
                                                m.KXG08_INT_PIN_CTL_IEL1_MASK)                       # both int pins active

    ## change mode (manual)
    sensor.wake_sleep(WAKE)
    #sensor.wake_sleep(SLEEP)
    
    ## power sensor(s    
    #
    #Turn on operating mode (disables setup)
    #
    
    if power_off_on:
        sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP )                # acc + gyro + temp ON

    #sensor.register_dump()#;sys.exit()

    logger.info('enable_data_logging done')

def read_with_polling(sensor, loop):
    count = 0
    timing.reset()
    print start_time_str()
    
    # print log header    
    print (DELIMITER.join(['#timestamp','10','temperature','gx','gy','gz','ax','ay','az']))
    
    try:
        while count < loop or loop is None:
            count += 1
            sensor.drdy_function()

            now = timing.time_elapsed()          
            temp, gx, gy, gz, ax, ay, az = sensor.read_data(CH_GYRO | CH_ACC | CH_TEMP)

            print ('{:.6f}{}10{}'.format(now, DELIMITER, DELIMITER) +
                   DELIMITER.join('{:d}'.format(t) for t in [temp, gx, gy, gz, ax, ay, az]))
    
    except KeyboardInterrupt:
        print end_time_str()

def read_with_stream(sensor, loop):
    stream = kxg08_data_stream(sensor)
    stream.read_data_stream(loop)
    return stream
    
def logger_main():
    
    sensor = kxg08_driver()

    bus = open_bus_or_exit(sensor)    
    enable_data_logging(sensor)
    
    timing.reset()
    if args.stream_mode:
        read_with_stream(sensor, args.loop)
    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    bus.close()
    
if __name__ == '__main__':
    logger_main()
