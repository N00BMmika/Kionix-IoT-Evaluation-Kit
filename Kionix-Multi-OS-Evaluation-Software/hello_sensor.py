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
import sys, time
from lib.bus_base import BusException
from lib.util_lib import logger, evkit_config
from connection_setup import setup_default_connection

#import all supported sensor drivers
from kx126.imports import kx126_driver
from kx022_kx122.imports import kx022_driver
from kmx62.imports import kmx62_driver
from kxg03.imports import kxg03_driver
from kxg08.imports import kxg08_driver
from kxtj2.imports import kxtj2_driver
from kxtj3.imports import kxtj3_driver
from kxcnl.imports import kxcnl_driver

from bh1726.imports import bh1726_driver
from bh1730.imports import bh1730_driver
from bh1745.imports import bh1745_driver
from bh1790.imports import bh1790_driver
#from bh1792.imports import bh1792_driver  # commented out, because bh1792 is not included in release 1.1
from bm1383glv.imports import bm1383glv_driver
from bm1383aglv.imports import bm1383aglv_driver
from bm1422gmv.imports import bm1422gmv_driver
from rpr0521.imports import rpr0521_driver


def test_default():
    # list of all supported sensor drivers
    bus = None
    sensors = [
        kx126_driver(),
        kx022_driver(),
        kmx62_driver(),
        kxg03_driver(),
        kxg08_driver(),
        kxtj2_driver(),
        kxtj3_driver(),
        kxcnl_driver(),
        bh1726_driver(),
        bh1730_driver(),
        bh1745_driver(),
        bh1790_driver(),
        #bh1792_driver(),   # commented out, because bh1792 is not included in release 1.1
        bm1383glv_driver(),
        bm1383aglv_driver(),
        bm1422gmv_driver(),
        rpr0521_driver(),
        ]

    # Get first available sensor on default bus.
    bus = setup_default_connection()

    # por not needed
##    # reset all found sensors -> int lines should go active high
##    for sensor in sensors:
##            if bus.probe_sensor(sensor):
##                logger.debug('%s found sensor, run POR function' % sensor.name)
##                sensor.por()

    for sensor in sensors:
        #logger.info('Looking for sensor with "%s".' % sensor.name)
        try:
            found = bus.probe_sensor(sensor)

            #bus = setup_default_connection(sensor)

            if not found:
                # no sensors found
                #logger.info('No sensors found')
                continue

            #logger.debug('Sensor found')
            read_sensor_data(sensor)

        except BusException,e:
            #Sensor not found.
            logger.info(e)
            continue

        except Exception,e:
            logger.info('Hello Sensor got exception %s ' % e)
            continue
            
    bus.close()


def read_sensor_data(sensor):
    print('Reading 10 data samples with %s.' % sensor.name)

    try:
        sensor.por()
        sensor.set_default_on()
        #sensor.register_dump()
        
        for t in range(10):
            print t,sensor.read_data()

            # wait for new data
            ## todo use definition from settings.cfg
            try:
                sensor.drdy_function()
            except NotImplementedError:
                time.sleep(0.1)
                pass


    finally:
        sensor.set_power_off()    

if __name__ == '__main__':
    if evkit_config.get('generic', 'drdy_operation') != 'INTERVAL_READ':
        logger.warning('***** drdy_operation != INTERVAL_READ. If interrupts not configured properly then data is not received')
    
    test_default()
