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
from imports import *

LOW_POWER_MODE = False

def enable_data_logging(sensor):
    ## set odrs
    sensor.set_odr(b.KXG03_ACCEL_ODR_WAKE_ODRA_W_25,
                   b.KXG03_ACCEL_ODR_SLEEP_ODRA_S_25, CH_ACC)       # wake and sleep
    sensor.set_odr(b.KXG03_GYRO_ODR_WAKE_ODRG_W_25, 
                   b.KXG03_GYRO_ODR_SLEEP_ODRG_S_25, CH_GYRO)       # wake and sleep

    ## select ranges
    sensor.set_range(b.KXG03_ACCEL_CTL_ACC_FS_W_2G,
                     b.KXG03_ACCEL_CTL_ACC_FS_S_2G, CH_ACC)         # wake and sleep
    sensor.set_range(b.KXG03_GYRO_ODR_WAKE_GYRO_FS_W_1024,
                     b.KXG03_GYRO_ODR_SLEEP_GYRO_FS_S_1024, CH_GYRO)  # wake and sleep

    ## averaging for acc and BW for gyro
    sensor.set_average(b.KXG03_ACCEL_ODR_WAKE_NAVG_W_128_SAMPLE_AVG,
                       b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_2_SAMPLE_AVG, CH_ACC)  # only in low power mode, for wake and sleep modes
    sensor.set_BW(b.KXG03_GYRO_ODR_WAKE_GYRO_BW_W_10,
                  b.KXG03_GYRO_ODR_SLEEP_GYRO_BW_S_10, CH_GYRO)     # wake and sleep

    ## interrupts
    sensor.write_register(r.KXG03_INT_PIN1_SEL, 0)                  # routing 0
    sensor.write_register(r.KXG03_INT_MASK1, 0)                     # mask 0
    sensor.write_register(r.KXG03_INT_PIN2_SEL, 0)                  # routing 0

    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(1, CH_ACC)                                   # acc data ready to int1
        # sensor.enable_drdy(1, CH_GYRO)                                 # gyro data ready to int1

    elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
        sensor.enable_drdy(2, CH_ACC)                                   # acc data ready to int2
        # sensor.enable_drdy(2, CH_GYRO)                                 # gyro data ready to int2

    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        # drdy must be enabled also when polling
        sensor.enable_drdy(1, CH_ACC)
        #sensor.enable_drdy(1, CH_GYRO)

    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        IEA1 = b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_HIGH
        IEA2 = b.KXG03_INT_PIN_CTL_IEA2_ACTIVE_HIGH
    else:
        IEA1 = b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_LOW
        IEA2 = b.KXG03_INT_PIN_CTL_IEA2_ACTIVE_LOW

    sensor.write_register(r.KXG03_INT_PIN_CTL, b.KXG03_INT_PIN_CTL_IEN2             |
                                               IEA2 |
                                               b.KXG03_INT_PIN_CTL_IEL2_LATCHED     |
                                               b.KXG03_INT_PIN_CTL_IEN1             |
                                               IEA1 |
                                               b.KXG03_INT_PIN_CTL_IEL1_LATCHED)    # both int pins active + latched

    ## power modes can be mixed also
    if LOW_POWER_MODE == True:
        power_modes(sensor, LPMODE, WAKE)
        power_modes(sensor, LPMODE, SLEEP)
        sensor.set_average( b.KXG03_ACCEL_ODR_WAKE_NAVG_W_128_SAMPLE_AVG, \
                            b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_32_SAMPLE_AVG, CH_ACC)
        #sensor.set_average( b.KXG03_ACCEL_ODR_WAKE_NAVG_W_4_SAMPLE_AVG, \
        #                    b.KXG03_ACCEL_ODR_SLEEP_NAVG_S_NO_AVG, CH_ACC)         
    else:
        power_modes(sensor, FULL_RES, WAKE)
        power_modes(sensor, FULL_RES, SLEEP)
        
    ## change mode (for start)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)

    ## power sensor(s)
    #sensor.set_power_on(CH_ACC | CH_GYRO )                         # acc + gyro ON
    sensor.set_power_on(CH_ACC | CH_GYRO | CH_TEMP)                # acc + gyro + temp ON

    #sensor.register_dump()

    sensor.release_interrupts(1)                                    # clear int 1
    sensor.release_interrupts(2)                                    # clear int 2
    sensor.read_data()                                              # this latches data ready interrupt register and signal
    logger.debug('init_data_logging done')

def readAndPrint(sensor):
    # wait for new data
    sensor.drdy_function()
    now = timing.time_elapsed()
    if 0:  # gyro + acc data
        data = sensor.read_data(CH_GYRO | CH_ACC)
        print '%f%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
                                              data[0], DELIMITER,
                                              data[1], DELIMITER,
                                              data[2], DELIMITER,
                                              data[3], DELIMITER,
                                              data[4], DELIMITER,
                                              data[5])          # output order; gyro, acc
    else:  # temp+gyro+acc data
        data = sensor.read_data(CH_TEMP | CH_GYRO | CH_ACC)
        print '%f%s%d%s%d%s%d%s%d%s%d%s%d%s%d' % (now, DELIMITER,
                                                  data[0], DELIMITER,
                                                  data[1], DELIMITER,
                                                  data[2], DELIMITER,
                                                  data[3], DELIMITER,
                                                  data[4], DELIMITER,
                                                  data[5], DELIMITER,
                                                  data[6])          # output order; temp, gyro, acc

def read_with_polling(sensor, loop):
    try:
        if loop is None:
            while True:
                readAndPrint(sensor)
        else:
            for i in range(loop):
                readAndPrint(sensor)

    except (KeyboardInterrupt):
        pass

def read_with_stream(sensor, loop):
    count = 0
    # experimental implementation of data streaming
    assert evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT', 'ADAPTER_GPIO2_INT'], 'An Int pin must be configured in order to use streaming.'
   
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        gpio_pin = sensor._bus._gpio_pin_index[0]
    else:
        gpio_pin = sensor._bus._gpio_pin_index[1]
    
    resp=sensor._bus.enable_interrupt(gpio_pin, [sensor.address(), r.KXG03_GYRO_XOUT_L, 12])

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
                print now, l

            count += 1

    except KeyboardInterrupt:
        pass
    
    finally:
        logger.debug("Disable interupt request")
        sensor._bus._flush_input()
        resp=sensor._bus.disable_interrupt(gpio_pin)
        logger.debug("Disable interupt done")
 
if __name__ == '__main__':
    sensor = kxg03_driver()
    bus = open_bus_or_exit(sensor)
    enable_data_logging(sensor)
    timing.reset()
    try:
        if args.stream_mode:
            read_with_stream(sensor, args.loop)
        else:
            read_with_polling(sensor, args.loop)
    finally:
        sensor.set_power_off()
        bus.close()
