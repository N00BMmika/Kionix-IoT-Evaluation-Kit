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
## basic data logger for KXTJ2
###
## Data ready is only GPIO-1_INT
## DRDY INT must be released separately with INT_REL
###

from imports import *

class stream_config:
    def __init__(self, sensor):
        assert evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT'], 'An Int pin1 must be configured in order to use streaming.'
        self.gpio_pin = sensor._bus._gpio_pin_index[0]
        
        self.fmt = "<Bhhhb"
        self.hdr = "ch!ax!ay!az"
        self.msg = [self.gpio_pin, [sensor.address(), r.KXTJ2_OUTX_L, 6,
                                    sensor.address(), r.KXTJ2_INT_REL, 1,]]

def enable_data_logging(sensor, odr = 25):
    logger.debug('enable_data_logging start')
    sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settings

    ## select ODR
    odr = convert_to_enumkey(odr)
    sensor.set_odr(e.KXTJ2_DATA_CTRL_REG_OSA[odr])  # odr setting for basic data logging
    
    ## select g-range
    sensor.set_range(b.KXTJ2_CTRL_REG1_GSEL_2G)
    #sensor.set_range(b.KXTJ2_CTRL_REG1_GSEL_4G)
    #sensor.set_range(b.KXTJ2_CTRL_REG1_GSEL_8G)
    #sensor.set_range(b.KXTJ2_CTRL_REG1_GSEL_8G_14B)   # 8g -range with 14b data

    ## resolution / power mode selection
    LOW_POWER_MODE = False
    if LOW_POWER_MODE == True:
        sensor.reset_bit(r.KXTJ2_CTRL_REG1, b.KXTJ2_CTRL_REG1_RES)# low power mode  
    else:
        sensor.set_bit(r.KXTJ2_CTRL_REG1, b.KXTJ2_CTRL_REG1_RES)# high resolution mode
      
    ## interrupts settings
    ## select dataready routing for sensor = int1 or register polling
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy()
        sensor.set_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEN)    # enable interrrupt pin    
    elif evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy()                # drdy must be enabled also when register polling
    ## interrupt signal parameters
    sensor.reset_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEL)  # latched interrupt
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEA) # active high
    else:
        sensor.reset_bit(r.KXTJ2_INT_CTRL_REG1, b.KXTJ2_INT_CTRL_REG1_IEA)# active low

    sensor.set_power_on()

    #sensor.register_dump()#; sys.exit()

    logger.debug('init_data_logging done')

    sensor.release_interrupts()
    
def read_with_polling(sensor, loop):
    ## HOX! data is in raw 16b mode   
    count = 0

    try:
        while count < loop or loop is None:        

            # wait for new data
            sensor.drdy_function()
            now = timing.time_elapsed()
            x,y,z = sensor.read_data()
            print '%f%s%d%s%d%s%d' %  (now,DELIMITER,x,DELIMITER,y,DELIMITER,z)
            
            ## need to release explicitely if monitoring drdy interrupt line
            sensor.release_interrupts()
            count +=1
            
    except KeyboardInterrupt:
        pass
    
    finally:
        logger.debug("Bye")        

def read_with_stream(sensor, loop):
    ## HOX! data is in raw 16b mode      
    count = 0
    data_received = False
    
    cfg = stream_config(sensor)
    resp=sensor._bus.enable_interrupt(*cfg.msg)
  
    try:
        while count < loop or loop is None:
            resp = sensor._bus.wait_indication()

            if resp is None:
                logger.warning("timeout")
            elif len(resp) !=8:
                logger.warning("Wrong message length %d" % len(resp) )            
            else:
                data_received = True
                now = timing.time_elapsed()
                data = struct.unpack(cfg.fmt, resp)[1:]                

                print '%f%s%d%s%d%s%d' % (now, DELIMITER,
                                          data[0], DELIMITER,
                                          data[1], DELIMITER,
                                          data[2])
            count += 1
     
    except KeyboardInterrupt:
        pass
    
    finally:
        if not data_received:
            logger.error("No stream data received")
            
        logger.debug("Disable interrupt request")
        resp=sensor._bus.disable_interrupt(cfg.gpio_pin)
        logger.debug("Disable interrupt done")

if __name__ == '__main__':
    sensor=kxtj2_driver()
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
