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
from imports import *
from kx126_pedometer import Pedometer_parameters_odr_50,Pedometer_parameters_odr_100
from kx126_pedometer import enable_data_logging
'''
Starts pedometer step count 
Doesnt power off the sensor when finished
'''


_CODE_FORMAT_VERSION = 2.0


def start_step_count(sensor,
                    cfg = Pedometer_parameters_odr_100,
                    odr = 100, 
                    avg = 128,
                    power_off_on = True):
    enable_data_logging(sensor, cfg = cfg, odr = odr, avg=avg)
    #
    # Power on the sensor (disables setup)
    #
    if power_off_on:
        sensor.set_power_on()
    logger.info('Step counter initialized')
    
def app_main():
    sensor = kx126_driver()
    bus = open_bus_or_exit(sensor)
    start_step_count(sensor)
    bus.close()

    
if __name__ == '__main__':
    app_main()