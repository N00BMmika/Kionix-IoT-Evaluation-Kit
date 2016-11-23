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

def test_data_logging(pressure_sensor):
    """
    Measuring one measurement at the time. Loop it until stopped.
    """
    try:
        pressure_sensor.set_default_on()
        pressure_sensor.stop_measurement()

        #Check bm1383aglv.py for measurement times for different averaging setup.
        #drdy_poll_interval typical value 100ms. 50ms is ok.
        pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_SINGLE)
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_2_TIMES)
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_4_TIMES)
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_8_TIMES)
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_16_TIMES)
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_32_TIMES)   #drdy_poll_interval must be >= 80ms
        #pressure_sensor.set_averaging(b.BM1383_MODE_CONTROL_REG_AVE_NUM_64_TIMES)   #drdy_poll_interval must be >= 158ms

        pressure_sensor.disable_drdy_pin()

        while 1:
            pressure_sensor.start_oneshot_measurement()
            pressure_sensor.drdy_function()      # follows the configuration from settings.cfg

            now_ms = int(time.clock()*1000)
            ## SI-unit data reading (3 decimals)
            c0,c1 = pressure_sensor.read_temperature_pressure()
            print '%d%s%2.03f%s%2.03f' %  (now_ms,DELIMITER,c0,DELIMITER,c1)

    except KeyboardInterrupt:
        pass
    finally:
        pressure_sensor.set_power_off()    

if __name__ == '__main__':
    pressure_sensor=bm1383aglv_driver()
    bus = open_bus_or_exit(pressure_sensor)
    test_data_logging(pressure_sensor)
    bus.close()
