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

_CODE_FORMAT_VERSION = 2.0
'''
Reads stepcount register
After register is read, stepcount is set to 0
'''

def read_step_count(sensor,
                    power_off_on = False):

    logger.info('read_step_count initialized')
    steps = sensor.read_step_count()
    if power_off_on:
        sensor.set_power_off()
    print 'Steps counted: %s' %steps
    return steps

def app_main():
    sensor = kx126_driver()
    #NOTE: Dont pass sensor instance to setup_default_connection to avoid por
    bus = setup_default_connection(skip_board_init = True)
    bus.probe_sensor(sensor)
    read_step_count(sensor)
    bus.close()

if __name__ == '__main__':
    app_main()    
    

