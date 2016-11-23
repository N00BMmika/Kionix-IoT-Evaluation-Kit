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
## KMX62 logger application
##
###

LOW_POWER_MODE = False

from imports import *

def init_data_logging(sensor):
    logger.debug('init_data_logging start')
    
    sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings
    # Select acc ODRs
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_0P781, CH_ACC)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_1P563, CH_ACC)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_3P125, CH_ACC)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_6P25, CH_ACC)                 # set OD
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_12P5, CH_ACC)                 # set ODR
    sensor.set_odr(b.KMX62_ODCNTL_OSA_25, CH_ACC)                   # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_50, CH_ACC)                   # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_100, CH_ACC)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_200, CH_ACC)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_400, CH_ACC)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_800, CH_ACC)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_1600, CH_ACC)                 # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_25K6ST0P8, CH_ACC)            # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_25K6ST1P6, CH_ACC)            # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSA_25K6ST3P2, CH_ACC)            # set ODR

    # Select mag ODRs
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_0P781, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_1P563, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_3P125, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_6P25, CH_MAG)                 # set OD
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_12P5, CH_MAG)                 # set ODR
    sensor.set_odr(b.KMX62_ODCNTL_OSM_25, CH_MAG)                   # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_50, CH_MAG)                   # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_100, CH_MAG)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_200, CH_MAG)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_400, CH_MAG)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_800, CH_MAG)                  # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_1600, CH_MAG)                 # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_12K8A, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_12K8B, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_12K8C, CH_MAG)                # set ODR
    #sensor.set_odr(b.KMX62_ODCNTL_OSM_12K8, CH_MAG)                 # set ODR

    # select g-range (for acc)
    sensor.set_range(b.KMX62_CNTL2_GSEL_2G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_4G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_8G, CH_ACC)
    #sensor.set_range(b.KMX62_CNTL2_GSEL_16G, C_ACC)
    
    ## power mode (accelerometer and magnetometer)
    if LOW_POWER_MODE:
        sensor.set_average(b.KMX62_CNTL2_RES_A4M2, None, CH_ACC)
        sensor.set_average(b.KMX62_CNTL2_RES_A32M16, None, CH_ACC)
    else:
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2,None, CH_ACC)
            
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
            IEA1 = b.KMX62_INC3_IEA1_HIGH
        else:
            IEA1 = b.KMX62_INC3_IEA1_LOW
            
        sensor.write_register(r.KMX62_INC3,
                              b.KMX62_INC3_IEL1_LATCHED |
                              IEA1 |
                              b.KMX62_INC3_IED1_PUSHPULL
                              )
        sensor.enable_drdy(1, CH_ACC)                       # acc data ready to int1
        #sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
        
    elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
        if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
            IEA2 = b.KMX62_INC3_IEA2_HIGH
        else:
            IEA2 = b.KMX62_INC3_IEA2_LOW

        sensor.write_register(r.KMX62_INC3,
                              b.KMX62_INC3_IEL2_LATCHED |
                              IEA2 |
                              b.KMX62_INC3_IED2_PUSHPULL
                              )
        sensor.enable_drdy(2, CH_ACC)                       # acc data ready to int2
        #sensor.enable_drdy(2, CH_MAG)                       # mag data ready to int2    


    # start measurement
    #sensor.set_power_on(CH_MAG )              # mag ON
    #sensor.set_power_on(CH_ACC | CH_MAG )              # acc + mag ON
    sensor.set_power_on(CH_ACC | CH_MAG | CH_TEMP)     # acc + mag + temp ON

    #sensor.register_dump()
    
    logger.debug('init_data_logging done')    
    sensor.read_data()                              # this latches data ready interrupt register and signal
    sensor.release_interrupts()                     # clear all internal function interrupts

def readAndPrint(sensor):
    # wait for new data
    sensor.drdy_function()
    now = timing.time_elapsed()
    if 0: # mag data only
        data = sensor.read_data(CH_MAG)
        print '%f%s%d%s%d%s%d' % (now, DELIMITER,
                                              data[0], DELIMITER,
                                              data[1], DELIMITER,
                                              data[2])
##        print '%f%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
##                                              data[0], DELIMITER,
##                                              data[1], DELIMITER,
##                                              data[2], DELIMITER,
##                                              data[3], DELIMITER,
##                                              data[4], DELIMITER,
##                                              data[5])        
    else: # print acc + mag + temp data
        data = sensor.read_data(CH_ACC | CH_MAG | CH_TEMP)
        print '%f%s%d%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
                                                  data[0], DELIMITER,
                                                  data[1], DELIMITER,
                                                  data[2], DELIMITER,
                                                  data[3], DELIMITER,
                                                  data[4], DELIMITER,
                                                  data[5], DELIMITER,
                                                  data[6])


def read_with_polling(sensor, loop):
    try:
        if loop is None:
            while True:
                readAndPrint(sensor)
        else:
            for i in range(loop):
                readAndPrint(sensor)

    except KeyboardInterrupt:
        pass


def read_with_stream(sensor, loop):
    count = 0
    # experimental implementation of data streaming
    assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','This example supports only int1'
    gpio_pin = sensor._bus._gpio_pin_index[1-1]

    ## acc + mag
    resp=sensor._bus.enable_interrupt(gpio_pin, [sensor.address(), r.KMX62_ACCEL_XOUT_L, 12])

    ## mag only
    #resp=sensor._bus.enable_interrupt(gpio_pin, [sensor.address(), r.KMX62_MAG_XOUT_L, 6])    
    #print 'resp',[hex(ord(t)) for t in resp]

    try:
        while count < loop or loop is None:
            resp = sensor._bus.wait_indication()          
            if resp is None:
                logger.info("timeout")
                continue

            now = timing.time_elapsed()

            ## acc + mag
            data = struct.unpack('<Bhhhhhh',resp)[1:]

            ## mag only

            #data = struct.unpack('<Bhhh',resp)[1:]
             
            l = len(data)
 
            if l == 6:
                print '%f%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
                                                      data[0], DELIMITER,
                                                      data[1], DELIMITER,
                                                      data[2], DELIMITER,
                                                      data[3], DELIMITER,
                                                      data[4], DELIMITER,
                                                      data[5])
            elif l == 3:
                print '%f%s%d%s%d%s%d%s' % (now, DELIMITER,
                                                      data[0], DELIMITER,
                                                      data[1], DELIMITER,
                                                      data[2], DELIMITER)
            else:
                logger.warning("Wrong message length %d" % len(resp) )

            count += 1

    except KeyboardInterrupt:
        pass
    finally:
        logger.debug("Disable interrupt request")
        resp=sensor._bus.disable_interrupt(gpio_pin)
        logger.debug("Disable interrupt done")
    
if __name__ == '__main__':
    sensor = kmx62_driver()
    bus = open_bus_or_exit(sensor)
    init_data_logging(sensor)
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
