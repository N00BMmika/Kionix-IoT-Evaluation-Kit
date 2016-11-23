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
## data logger application for KXG07 and KXG08
###

LOW_POWER_MODE = False

from imports import *

def enable_data_logging(sensor):
    logger.debug('init_data_logging start')    
    ## set odrs
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_0P781, None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_1P563, None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_3P125, None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_6P25,  None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_12P5,  None, CH_ACC)      # acc odr
    sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_25,    None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_50,    None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_100,   None, CH_ACC)      # acc odr        
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_200,   None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_400,   None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_800,   None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_1600,  None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_3200,   None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_6400,   None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_12800,  None, CH_ACC)      # acc odr
    #sensor.set_odr(b.KXG08_ACCEL_ODR_ODRA_25600,  None, CH_ACC)      # acc odr

    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_0P781,  None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_1P563,  None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_3P125,  None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_6P25,   None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_12P5,   None, CH_GYRO)     # gyro odr
    sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_25,     None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_50,     None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_100,    None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_200,    None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_400,    None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_1600,   None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_3200,    None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_6400,    None, CH_GYRO)     # gyro odr
    #sensor.set_odr(b.KXG08_GYRO_ODR_ODRG_12800,   None, CH_GYRO)     # gyro odr

    ## select ranges
    sensor.set_range(b.KXG08_ACCEL_CTL_ACC_FS_2G,  None, CH_ACC)    # acc range
    #sensor.set_range(b.KXG08_ACCEL_CTL_ACC_FS_4G,  None, CH_ACC)    # acc range
    #sensor.set_range(b.KXG08_ACCEL_CTL_ACC_FS_8G,  None, CH_ACC)    # acc range
    #sensor.set_range(b.KXG08_ACCEL_CTL_ACC_FS_16G, None, CH_ACC)    # acc range
    
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_64,   None, CH_GYRO)  # gyro range
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_128,  None, CH_GYRO)  # gyro range
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_256,  None, CH_GYRO)  # gyro range
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_512,  None, CH_GYRO)  # gyro range
    sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_1024, None, CH_GYRO)  # gyro range
    #sensor.set_range(b.KXG08_GYRO_CTL_GYRO_FS_2048, None, CH_GYRO)  # gyro range

    if LOW_POWER_MODE:
        power_modes(sensor, LPMODE, None, CH_ACC)                  # power mode for acc 
        power_modes(sensor, LPMODE, None, CH_GYRO)                 # power mode for gyro            
        ## averaging 
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG, CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_64_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_32_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_16_SAMPLE_AVG,  CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_8_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_4_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        #sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_2_SAMPLE_AVG,   CH_ACC)      # acc low power mode
        sensor.set_average(b.KXG08_ACCEL_ODR_NAVGA_NO_AVG,         CH_ACC)      # acc low power mode
        ## averaging for gyro only with version 2080
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG, CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_64_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_32_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_16_SAMPLE_AVG,  CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_8_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_4_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        #sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_2_SAMPLE_AVG,   CH_GYRO)      # gyro low power mode
        sensor.set_average(b.KXG08_GYRO_ODR_NAVGG_NO_AVG,         CH_GYRO)      # gyro low power mode
    else:
        power_modes(sensor, FULL_RES, None, CH_ACC)                 # power mode for acc        
        power_modes(sensor, FULL_RES, None, CH_GYRO)                # power mode for gyro
        
    ## bandwidth
    #sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_2, CH_ACC)       # bandwidth acc      
    sensor.set_BW(b.KXG08_ACCEL_CTL_ACC_BW_ODR_8, CH_ACC)       # bandwidth acc 
    #sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_2, CH_GYRO)      # bandwidth gyro
    sensor.set_BW(b.KXG08_GYRO_CTL_GYRO_BW_ODR_8, CH_GYRO)      # bandwidth gyro

    ## interrupts
    sensor.write_register(r.KXG08_INT_PIN_SEL1, 0)              # routings off
    sensor.write_register(r.KXG08_INT_PIN_SEL2, 0)              # 
    sensor.write_register(r.KXG08_INT_PIN_SEL3, 0)              # 
    sensor.write_register(r.KXG08_INT_MASK1, 0)                 # masks all ints out
    
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(1, CH_ACC)                                   # acc data ready to int1
        #sensor.enable_drdy(1, CH_GYRO)                                 # gyro data ready to int1

    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':
        sensor.enable_drdy(2, CH_ACC)                                   # acc data ready to int2
        #sensor.enable_drdy(2, CH_GYRO)                                 # gyro data ready to int2

    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when polling
        sensor.enable_drdy(1, CH_ACC)

    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        IEA1 = b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH
        IEA2 = b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH
    else:
        IEA1 = b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW
        IEA2 = b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW

    sensor.write_register(r.KXG08_INT_PIN_CTL, b.KXG08_INT_PIN_CTL_IEN2             | \
                                               IEA2 | \
                                               b.KXG08_INT_PIN_CTL_IEL2_LATCHED     | \
                                               b.KXG08_INT_PIN_CTL_IEN1             | \
                                               IEA1 | \
                                               b.KXG08_INT_PIN_CTL_IEL1_LATCHED)    # both int pins active

    ## change mode (manual)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)
    
    ## power sensor(s)
    #sensor.set_power_on(CH_ACC )                                   # acc ON
    #sensor.set_power_on(CH_ACC | CH_GYRO )                         # acc + gyro ON
    sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP )                # acc + gyro + temp ON

    #sensor.register_dump()

    sensor.release_interrupts(1)                                    # clear int 1
    sensor.release_interrupts(2)                                    # clear int 2

    sensor.read_data()                                              # this latches data ready interrupt register and signal
    logger.debug('enable_data_logging done')

def readAndPrint(sensor):

    sensor.drdy_function()

    now = timing.time_elapsed()
    if 0: # time + gyro + acc data
        data = sensor.read_data( CH_GYRO | CH_ACC)
        print '%f%s%d%s%d%s%d%s%d%s%d%s%d' % (now,DELIMITER,  \
                                              data[0],DELIMITER, \
                                              data[1],DELIMITER, \
                                              data[2],DELIMITER, \
                                              data[3],DELIMITER, \
                                              data[4],DELIMITER, \
                                              data[5])             # output order; gyro, acc
    else: # time + temp + gyro + acc data
        data = sensor.read_data( CH_TEMP | CH_GYRO | CH_ACC )
        print '%f%s%d%s%d%s%d%s%d%s%d%s%d%s%d' % (now,DELIMITER,\
                                                  data[0],DELIMITER, \
                                                  data[1],DELIMITER, \
                                                  data[2],DELIMITER, \
                                                  data[3],DELIMITER, \
                                                  data[4],DELIMITER, \
                                                  data[5],DELIMITER, \
                                                  data[6])              # output order; temp, gyro, acc

def read_with_polling(sensor, loop):
    try:
        if loop == None:
            while 1:
                readAndPrint(sensor)
        else:
            for i in range(loop):
                readAndPrint(sensor)

    except(KeyboardInterrupt):
        pass

def read_with_stream(sensor, loop):
    count = 0
    # experimental implementation of data streaming
    assert evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT', 'ADAPTER_GPIO2_INT'], 'An Int pin must be configured in order to use streaming.'

    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        gpio_pin = sensor._bus._gpio_pin_index[0]
    else:
        gpio_pin = sensor._bus._gpio_pin_index[1]

    resp=sensor._bus.enable_interrupt(gpio_pin, [sensor.address(), r.KXG08_GYRO_XOUT_L, 12])

    try:
        while count < loop or loop is None:
            resp = sensor._bus.wait_indication()
            now = timing.time_elapsed()

            data = struct.unpack('<Bhhhhhh',resp)[1:]
            l = len(data)
            if l == 6:
                print '%f%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
                                                      data[0], DELIMITER,
                                                      data[1], DELIMITER,
                                                      data[2], DELIMITER,
                                                      data[3], DELIMITER,
                                                      data[4], DELIMITER,
                                                      data[5])

            else:
                logger.warning("Wrong message length %d" % len(resp) )

            count += 1

    except KeyboardInterrupt:
        pass
    
    finally:
        logger.debug("Disable interrupt request")
        sensor._bus._flush_input()        
        resp=sensor._bus.disable_interrupt(gpio_pin)
        logger.debug("Disable interrupt done")
    
if __name__ == '__main__':
    sensor = kxg08_driver()
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
        
    logger.info('bye')
    sensor.set_power_off()
    bus.close()
