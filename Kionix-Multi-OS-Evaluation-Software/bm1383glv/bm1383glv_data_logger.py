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

def init_data_logging(pressure_sensor):
    try:
        pressure_sensor.set_default_on()
        #pressure_sensor.set_odr(b.BM1383GLV_MODE_CONTROL_REG_MODE_50MS)
        #pressure_sensor.set_odr(b.BM1383GLV_MODE_CONTROL_REG_MODE_100MS)
        pressure_sensor.set_odr(b.BM1383GLV_MODE_CONTROL_REG_MODE_200MS)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_SINGLE)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_2_TIMES)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_4_TIMES)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_8_TIMES)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_16_TIMES)
        #pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_32_TIMES)
        pressure_sensor.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_64_TIMES)

        pressure_sensor.set_pressure_int_lower_treshold_raw(50000)
        pressure_sensor.set_pressure_int_upper_treshold_raw(50)
        pressure_sensor.enable_pressure_treshold_interrupts()
        
        status = pressure_sensor.ic_test()
        if (status != True):
            logger.debug("ic_test failed")
        
    except(KeyboardInterrupt):
        pressure_sensor.set_power_off()

def readAndPrint(pressure_sensor):

        pressure_sensor.drdy_function()      # follows the configuration from settings.cfg
        pressure_sensor.clear_interrupt() 
        now = timing.time_elapsed()

        ## Raw data reading
        #c0,c1,c2,c3,c4 = pressure_sensor.read_data_raw()
        #print '%d%s%d%s%d%s%d%s%d%s%d' %  (now_ms,DELIMITER,c0,DELIMITER,c1,DELIMITER,c2,DELIMITER,c3,DELIMITER,c4)
        ## SI-unit data reading (3 decimals)
        c0,c1 = pressure_sensor.read_temperature_pressure()
        print '%f%s%2.03f%s%2.03f' %  (now,DELIMITER,c0,DELIMITER,c1)

def read_with_polling(pressure_sensor, loop):
    try:
        if loop == None:
            while 1:
                readAndPrint(pressure_sensor)
        else:
            for i in range(loop):
                readAndPrint(pressure_sensor)
    except(KeyboardInterrupt):
        pass

if __name__ == '__main__':
    pressure_sensor=bm1383glv_driver()
    bus = open_bus_or_exit(pressure_sensor)
    init_data_logging(pressure_sensor)
    timing.reset()
    try:
        assert args.stream_mode == False, "Streaming not implemented yet."
        read_with_polling(pressure_sensor, args.loop)
    finally:
        pressure_sensor.set_power_off()
        bus.close()
