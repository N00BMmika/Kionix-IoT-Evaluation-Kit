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
from lib.util_lib import evkit_config, logger
from lib.bus_base import BusException

def setup_aardvark_spi(sensor=None):
    from lib import bus_aardvark   
    b=bus_aardvark.bus_aadvark_spi()
    cfg=b.get_configuration_template()    
    b.configure(cfg)
    b.open()
    if not sensor: return b
    
    if not b.probe_sensor(sensor):
        b.close()
        raise BusException('Bus not assigned to sensor.')
        return
    sensor.por()
    return b
    
def setup_aardvark_i2c(sensor=None):
    from lib import bus_aardvark   
    b=bus_aardvark.bus_aadvark_i2c()    
    cfg=b.get_configuration_template()  #get clock speed and bus timeout value
    b.configure(cfg)                    #set clock speed
    b.open()                            #open and configure bus
    if not sensor: return b

    if not b.probe_sensor(sensor):
        b.close()
        raise BusException('Bus not assigned to sensor.')
    sensor.por()
    return b

def setup_socket_i2c(sensor=None):
    from lib import bus_adb_socket
    b=bus_adb_socket.bus_adb_socket()    
    cfg=b.get_configuration_template()
    b.configure(cfg)
    b.open()
    if not sensor: return b

    if not b.probe_sensor(sensor):        
        b.close()
        raise BusException('Bus not assigned to sensor.')
        return None
    sensor.por()    
    return b

def setup_linux_i2c(sensor=None):
    from lib import bus_linux
    b=bus_linux.bus_linux_i2c()
    b.open()
    if not sensor: return b

    if not b.probe_sensor(sensor):
        b.close()
        raise BusException('Bus not assigned to sensor.')
        return None
    sensor.por()
    return b

def setup_serial_i2c(sensor=None):
    from lib import bus_serial
    b=bus_serial.bus_serial_com()
    cfg=b.get_configuration_template()
    b.configure(cfg)
    b.open()
    if not sensor: return b

    if not b.probe_sensor(sensor):
        b.close()
        raise BusException('Bus not assigned to sensor.')
        return None
    sensor.por()    
    return b
    
def setup_default_connection(sensor=None):
    # This will create connection using connection defined in settings.cfg
    bus_index_dict={
        1:setup_aardvark_i2c,
        2:setup_aardvark_spi,
        3:setup_socket_i2c,
        4:setup_linux_i2c,
        5:setup_serial_i2c
        }

    bus_index = evkit_config.get('connection', 'bus_index')
    if bus_index.startswith('serial_com'):
        evkit_config.remove_section('__com__')
        evkit_config.add_section('__com__')
        evkit_config.set('__com__','config',bus_index)
        logger.info('Bus %s selected', bus_index)
        bus_index=5
    else:
        bus_index=int(bus_index)        
        logger.info('Bus index %d selected', bus_index)

    return bus_index_dict[bus_index](sensor)

def open_bus_or_exit(sensor):
    try:
        bus = setup_default_connection(sensor)
        # FIXME move after iot node init?
        
    except Exception, e:
        if str(e) == 'Bus not assigned to sensor.':
            logger.error(e)
        else:
            logger.critical(e)
            
        logger.warning('Try again.')
        raise
        exit()
        
    bus_index = evkit_config.get('connection', 'bus_index')

    if bus_index == '3' or bus_index == 'serial_com_kx_iot':
        logger.info('Kionix  IoT node init start')
        # FIXME do HW board config functionality and move this functionality there

        if evkit_config.get('generic', 'int1_active_high')!='FALSE' or \
           evkit_config.get('generic', 'int2_active_high')!='FALSE':
            logger.warning('Kionix IoT Board requires active low interrupts. Please update settings.cfg')
            #import sys
            #sys.exit(1)

        import kxg03
        from kxg03 import kxg03_driver
        kxg03 = kxg03_driver.kxg03_driver()
        if (bus.probe_sensor(kxg03)):
            logger.debug('Reset KXG03 and set interrput to active low')
            kxg03.por()
            #kxg03.set_power_off()
            #kxg03 inital settings for Kionix IoT Board
            kxg03.write_register(kxg03_driver.r.KXG03_INT_PIN_CTL, kxg03_driver.b.KXG03_INT_PIN_CTL_IEN2 | \
                                                      kxg03_driver.b.KXG03_INT_PIN_CTL_IEA2_ACTIVE_LOW   | \
                                                      kxg03_driver.b.KXG03_INT_PIN_CTL_IEL2_LATCHED      | \
                                                      kxg03_driver.b.KXG03_INT_PIN_CTL_IEN1              | \
                                                      kxg03_driver.b.KXG03_INT_PIN_CTL_IEA1_ACTIVE_LOW   | \
                                                      kxg03_driver.b.KXG03_INT_PIN_CTL_IEL1_LATCHED)    # both int pins active


        from kxg08 import kxg08_driver
        kxg08 = kxg08_driver.kxg08_driver()
        if (bus.probe_sensor(kxg08)):
            logger.debug('Reset KXG07/08 and set interrput to active low')
            kxg08.por()
            #kxg08.set_power_off()
            kxg08.write_register(kxg08_driver.r.KXG08_INT_PIN_CTL, kxg08_driver.b.KXG08_INT_PIN_CTL_IEN2 | \
                                                      kxg08_driver.b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW   | \
                                                      kxg08_driver.b.KXG08_INT_PIN_CTL_IEL2_LATCHED      | \
                                                      kxg08_driver.b.KXG08_INT_PIN_CTL_IEN1              | \
                                                      kxg08_driver.b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW   | \
                                                      kxg08_driver.b.KXG08_INT_PIN_CTL_IEL1_LATCHED)    # both int pins active

        from kx022_kx122 import kx022_driver
        kx122 = kx022_driver.kx022_driver()
        if (bus.probe_sensor(kx122)):
            logger.debug('Reset KX122 and set interrput to active low')
            kx122.por()
            #kx122.set_power_off()
            #KX122 inital settings for Kionix IoT Board
            kx122.reset_bit(kx022_driver.r122.KX122_INC1, kx022_driver.b122.KX122_INC1_IEA1) # active low int1
            kx122.reset_bit(kx022_driver.r122.KX122_INC5, kx022_driver.b122.KX122_INC5_IEA2) # active low int2
            #cntl1 = kx122.read_register(kx022_driver.r122.KX122_CNTL1)[0]
            #kx122.write_register(kx022_driver.r122.KX122_CNTL1, cntl1 | kx022_driver.b122.KX122_CNTL1_PC1)

        from bm1383glv import bm1383glv_driver
        bm1383glv = bm1383glv_driver.bm1383glv_driver()
        if (bus.probe_sensor(bm1383glv)):
            bm1383glv.por()

        from bm1383aglv import bm1383aglv_driver
        bm1383aglv = bm1383aglv_driver.bm1383aglv_driver()
        if (bus.probe_sensor(bm1383aglv)):
            bm1383aglv.por()
        
        logger.info('Kionix  IoT board init done')
        
    return bus

if __name__ == '__main__':
    pass
    # todo interactive tool for selecting connection 
