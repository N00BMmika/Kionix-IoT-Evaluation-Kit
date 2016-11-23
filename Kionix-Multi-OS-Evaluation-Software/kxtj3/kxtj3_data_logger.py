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

def init_data_logging(sensor):
    logger.debug('init_data_logging start')
    sensor.set_power_off()
        
    ## select ODR
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_0P781)  
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_1P563)  
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_3P125)  
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_6P25)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_12P5)
    sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_25)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_50)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_100)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_200)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_400)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_800)
    #sensor.set_odr(b.KXTJ3_DATA_CTRL_REG_OSA_1600)

    ## select g-range and measurement bits
    sensor.set_range(b.KXTJ3_CTRL_REG1_GSEL_2G)
    #sensor.set_range(b.KXTJ3_CTRL_REG1_GSEL_4G)
    #sensor.set_range(b.KXTJ3_CTRL_REG1_GSEL_8G)
    #sensor.set_range(b.KXTJ3_CTRL_REG1_GSEL_16G)
    #sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_EN16G)  # 16g and 14bits
    sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_EN16G) # other g's and 12bit
        
    ## resolution / power mode selection
    sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)# high resolution mode
    #sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)# low resolution mode        

    ## interrupts settings
    ## select dataready routing for sensor = int1 or register polling
    sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)    # enable interrrupt pin
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy()          
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy()                # drdy must be enabled also when register polling
    ## interrupt signal parameters
    sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEL)  # latched interrupt
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEA) # active high
    else:
        sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEA)# active low

    sensor.set_power_on()
    
    #sensor.register_dump()

    logger.debug('init_data_logging done')
def read_with_polling(sensor, loop):
    count = 0
    try:
        sensor.release_interrupts()

         ## selection of 12 and 14b data word length
        if (sensor.read_register(r.KXTJ3_CTRL_REG1, 1)[0] & b.KXTJ3_CTRL_REG1_EN16G) > 0:
            shift = 2
        else:
            shift = 4

        while count < loop or loop is None:
            # wait for new data
            sensor.drdy_function()
            now = timing.time_elapsed()
            x,y,z = sensor.read_data()

            print '%f%s%d%s%d%s%d' %  (now,DELIMITER,x>>shift,DELIMITER,y>>shift,DELIMITER,z>>shift)

            # need to release explicitely if monitoring drdy interrupt line
            #sensor.read_register(r.KXTJ2_INT_REL, 1)
            sensor.release_interrupts()

            count += 1

    except KeyboardInterrupt:
        pass

def read_with_stream(sensor, loop):
    count = 0
    addr = sensor.address()
    # experimental implementation of data streaming
    assert evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT','This example supports only int1'
    gpio_pin = sensor._bus._gpio_pin_index[1-1]

     ## selection of 12 and 14b data word length
    if (sensor.read_register(r.KXTJ3_CTRL_REG1, 1)[0] & b.KXTJ3_CTRL_REG1_EN16G) > 0:
        shift = 2
    else:
        shift = 4

    resp=sensor._bus.enable_interrupt(gpio_pin, [addr, r.KXTJ3_OUTX_L, 6, addr, r.KXTJ3_INT_REL, 1])
    #print 'resp',[hex(ord(t)) for t in resp]

    try:
        while count < loop or loop is None:
            resp = sensor._bus.wait_indication()
            now = timing.time_elapsed()

            data = struct.unpack('<Bhhhb',resp)[1:]
            l = len(data)
            if l == 4:
                x,y,z,rel=data
                print '%f%s%d%s%d%s%d' %  (now, DELIMITER,x>>shift,DELIMITER,y>>shift,DELIMITER,z>>shift)
            else:
                logger.warning("Wrong message length %d" % len(resp) )

            count+=1

    except KeyboardInterrupt:
        # todo catch KeyboardInterrupt in framework
        pass
    
    finally:
        logger.debug("Disable interrupt request")
        resp=sensor._bus.disable_interrupt(gpio_pin)
        logger.debug("Disable interrupt done")

if __name__ == '__main__':
    sensor=kxtj3_driver()
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
