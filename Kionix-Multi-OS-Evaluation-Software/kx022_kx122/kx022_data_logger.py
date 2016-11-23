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
## basic logger application
###
## logging polling or stream
###

from imports import *

LOW_POWER_MODE = False                              # full resolution or low power

def init_data_logging(sensor):
    logger.debug('init_data_logging start')
    sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings

    ## select ODR
    #sensor.set_odr(b.KX022_ODCNTL_OSA_0P781)       #      
    #sensor.set_odr(b.KX022_ODCNTL_OSA_1P563)       #
    #sensor.set_odr(b.KX022_ODCNTL_OSA_3P125)       #    
    #sensor.set_odr(b.KX022_ODCNTL_OSA_6P25)        #
    #sensor.set_odr(b.KX022_ODCNTL_OSA_12P5)        # 
    sensor.set_odr(b.KX022_ODCNTL_OSA_25)           # odr setting for basic data logging
    #sensor.set_odr(b.KX022_ODCNTL_OSA_50)          #
    #sensor.set_odr(b.KX022_ODCNTL_OSA_100)         # 
    #sensor.set_odr(b.KX022_ODCNTL_OSA_200)         # works with Aardvark + I2C
    #sensor.set_odr(b.KX022_ODCNTL_OSA_400)         # works with Aardvark + SPI
    #sensor.set_odr(b.KX022_ODCNTL_OSA_800)         #
    #sensor.set_odr(b.KX022_ODCNTL_OSA_1600)        #
    ##higher than 1600Hz ODR are only for KX122, KX112, KX123, KX124
    #sensor.set_odr(b122.KX122_ODCNTL_OSA_3200)     #
    #sensor.set_odr(b122.KX122_ODCNTL_OSA_6400)     #        
    #sensor.set_odr(b122.KX122_ODCNTL_OSA_12800)    #
    #sensor.set_odr(b122.KX122_ODCNTL_OSA_25600)    #
    
    ## select g-range
    sensor.set_range(b.KX022_CNTL1_GSEL_2G)
    #sensor.set_range(b.KX022_CNTL1_GSEL_4G)
    #sensor.set_range(b.KX022_CNTL1_GSEL_8G)
    
    ## resolution / power mode selection
    ## Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)  
    if LOW_POWER_MODE:
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)                          # low current
        sensor.set_average(b.KX022_LP_CNTL_AVC_NO_AVG)                              # lowest current mode average
    else:
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)                            # high resolution
         
    ## interrupts settings
    ## select dataready routing for sensor = int1, int2 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(intpin=1)
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':
        sensor.enable_drdy(intpin=2)            
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy(intpin=1)                # drdy must be enabled also when register polling
        
    ## interrupt signal parameters
    sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)  # latched interrupt
    sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)  # latched interrupt    
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEA1) # active high
    else:
        sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEA1)# active low
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEA2) # active high
    else:
        sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEA2)# active low
        
    sensor.set_power_on()                           # settings coming to valid and start measurements
    
    #sensor.register_dump()

    logger.debug('init_data_logging done')

    sensor.read_data()                              # this latches data ready interrupt register and signal
    
    sensor.release_interrupts()                     # clear all internal function interrupts
    
def readAndPrint(sensor):
    # wait for new data
    sensor.drdy_function()
    now = timing.time_elapsed()
    x,y,z = sensor.read_data()
    print '%f%s%d%s%d%s%d' % (now,DELIMITER,x,DELIMITER,y,DELIMITER,z)
            
def read_with_polling(sensor, loop):
    try:
        if loop == None:
            while 1:
                readAndPrint(sensor)
        else:
            for i in range (loop):
                readAndPrint(sensor)
    except(KeyboardInterrupt):
        pass
    finally:
        sensor.set_power_off()
        bus.close

def read_with_stream(sensor, loop):
    count = 0
    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        gpio_pin = sensor._bus._gpio_pin_index[0]

    elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
        gpio_pin = sensor._bus._gpio_pin_index[1]

    resp=sensor._bus.enable_interrupt(gpio_pin, [sensor.address(), r.KX022_XOUT_L, 6])
    
    try:
        while count < loop or loop is None:
            resp = sensor._bus.wait_indication()
            if resp is None:
                logger.info("timeout")
                continue
                
            now = timing.time_elapsed()

            if len(resp)==7:
                data = struct.unpack('<Bhhh',resp)

                msgid,x,y,z = data
                print '%f%s%d%s%d%s%d' % (now, DELIMITER,
                                          x, DELIMITER,
                                          y, DELIMITER,
                                          z)

            else:
                logger.warning("Wrong message length %d" % len(resp) )

            count += 1

    except KeyboardInterrupt:
        # todo catch KeyboardInterrupt in framework
        pass
    
    finally:
        logger.debug("Disable interrupt request")
        resp=sensor._bus.disable_interrupt(gpio_pin)
        logger.debug("Disable interrupt done")

if __name__ == '__main__':
    sensor = kx022_driver()
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
