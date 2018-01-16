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
import sys
from lib.util_lib import evkit_config, logger, ACTIVE_LOW
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
    from lib.bus_evkit import bus_socket
    b=bus_socket(index = 0)
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

def setup_socket_adb_i2c(sensor=None):
    from lib.bus_evkit import bus_socket
    b=bus_socket(index = 1)
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
    from lib.bus_evkit import bus_serial_com
    b=bus_serial_com()
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

def setup_linux_ble(sensor=None):
    from lib.bus_pygatt import bus_linux_ble
    b=bus_linux_ble()
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

def setup_raspberry_socket(sensor=None):
    "Socket connection to Raspberry Pi3 which is running Kionix Firmware"
    from lib.bus_evkit import bus_socket
    b=bus_socket(index=2)
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

def setup_default_connection(sensor=None, skip_board_init = False):
    # This will create connection using connection defined in settings.cfg
    bus_index_dict={
        1:setup_aardvark_i2c,
        2:setup_aardvark_spi,
        3:setup_socket_i2c,
        4:setup_linux_i2c,
        5:setup_socket_adb_i2c,
        6:setup_serial_i2c,
        7:setup_linux_ble,
        8:setup_raspberry_socket,
        }

    logger.debug('Python {}'.format(sys.version))
    bus_index = evkit_config.get('connection', 'bus_index')
    if  bus_index.startswith('serial_com'): 
        evkit_config.remove_section('__com__')
        evkit_config.add_section('__com__')
        evkit_config.set('__com__','config',bus_index)
        logger.info('Bus %s selected', bus_index)
        bus_index=6
    else:
        bus_index=int(bus_index)        
        logger.info('Bus index %d selected', bus_index)

    bus = bus_index_dict[bus_index](sensor)

    if not skip_board_init:
        ## Sensors in Kionix IoT node must be initialized to active low 
        if evkit_config.get('connection', 'bus_index') in ['3' , '5', '7','serial_com_kx_iot']:
            # FIXME nRF51-DK + BLE will cause board init, it is not needed

            logger.info('Kionix  IoT node init start')

            # FIXME add-on board detection with 1.4 firmware or later
            #addon_board = bus.gpio_read(8) # check if addon board is connected
            #if addon_board:                
            #    print "Add-on board found"
            addon_board = True # FIXME remove this for firmware 1.4 and later
            
            # FIXME do HW board config functionality and move this functionality there

            if evkit_config.get('generic', 'int1_active_high')!='FALSE' or \
               evkit_config.get('generic', 'int2_active_high')!='FALSE':
                logger.warning('Kionix IoT Board requires active low interrupts. Please update settings.cfg')

            import kxg03
            from kxg03 import kxg03_driver
            kxg03 = kxg03_driver.kxg03_driver()
            if (bus.probe_sensor(kxg03)):
                logger.debug('Reset KXG03 and set interrput to active low')
                kxg03.por()
                
                ## KXG03 inital settings for Kionix IoT Board
                kxg03.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)
                kxg03.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW)

            from kxg08 import kxg08_driver
            kxg08 = kxg08_driver.kxg08_driver()
            if (bus.probe_sensor(kxg08)):
                logger.debug('Reset KXG07/08 and set interrput to active low')
                kxg08.por()

                ## KXG08 inital settings for Kionix IoT Board
                kxg08.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)
                kxg08.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW)
                
            from kx022_kx122 import kx022_driver
            kx122 = kx022_driver.kx022_driver()
            if (bus.probe_sensor(kx122)):
                logger.debug('Reset KX122 set interrput to active low')
                kx122.por()
                
                ## KX122 inital settings for Kionix IoT Board
                kx122.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)
                kx122.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW)

            from kx126 import kx126_driver
            kx126 = kx126_driver.kx126_driver()
            if (bus.probe_sensor(kx126)):
                logger.debug('Reset KX126 and set interrput to active low')
                kx126.por()

                #KX126 inital settings for Kionix IoT Board
                kx126.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW)
                kx126.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW)

            #from bm1383glv import bm1383glv_driver
            #bm1383glv = bm1383glv_driver.bm1383glv_driver()
            #if (bus.probe_sensor(bm1383glv)):
            #    logger.debug('Reset BM1383GLV on main board and set interrput to active low')
            #    bm1383glv.por()

            from bm1383aglv import bm1383aglv_driver
            bm1383aglv = bm1383aglv_driver.bm1383aglv_driver()
            if (bus.probe_sensor(bm1383aglv)):
                logger.debug('Reset BM1383AGLV on main board and set interrput to active low')                
                bm1383aglv.por()

            ## sensor components on add-on boards
            if addon_board:        # add-on board found and settings for them

                from kx224 import kx224_driver
                kx224 = kx224_driver.kx224_driver()
                
                from kxtj3 import kxtj3_driver
                kxtj3 = kxtj3_driver.kxtj3_driver()
                                
                if (bus.probe_sensor(kx224)):
                    logger.debug('Reset KX224 on add-on board and set interrput to active low')
                    kx224.por()
                    
                    ## KX224 initial settings for Kionix IoT/Add-on Board
                    kx224.set_interrupt_polarity(intpin = 1, polarity = ACTIVE_LOW) # active low int1
                    kx224.set_interrupt_polarity(intpin = 2, polarity = ACTIVE_LOW) # active low int2

                elif (bus.probe_sensor(kxtj3)):
                    logger.debug('Reset KXTJ3 on add-on board and set interrput to active low')
                    kxtj3.por()
                    
                    ## KXTJ3 initial settings for Kionix IoT/Add-on Board
                    kxtj3.reset_bit(kxtj3_driver.r.KXTJ3_INT_CTRL_REG1, kxtj3_driver.b.KXTJ3_INT_CTRL_REG1_IEA)# active low
                    
                    
            logger.info('Kionix  IoT board init done')

    return bus

def open_bus_or_exit(sensor, skip_board_init = False):
    # FIXME remove this function. 
    try:
        bus = setup_default_connection(sensor = sensor, skip_board_init = skip_board_init )
        
    except Exception, e:
        if str(e) == 'Bus not assigned to sensor.':
            logger.error(e)
        else:
            logger.critical(e)
            
        logger.warning('Try again.')
        raise
        exit()
        
    return bus

if __name__ == '__main__':
    pass
    # todo interactive tool for selecting connection 
