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

def test_data_logging(dcs):
    """
    Test data logging, using configuration from settings.cfg. Configuration can be interval read or drdy reg polling.
    """
    try:
        #Setup for timer polling/drdy_reg_polling: default, just start measurement:
        dcs.set_default_on()

        now_ms = int(time.clock()*1000)
        print '%04d%s%s%s%s%s%s%s%s' %  (now_ms,DELIMITER,'     R',DELIMITER,'     G',DELIMITER,'     B',DELIMITER,'     C')
        while 1:
            dcs.drdy_function()            # settings.cfg is set to INTERVAL_READ OR DRDY_REG_POLL

            now_ms = int(time.clock()*1000)
            c0,c1,c2,c3 = dcs.read_data()
            print '%04d%s%6.d%s%6.d%s%6.d%s%6.d' %  (now_ms,DELIMITER,c0,DELIMITER,c1,DELIMITER,c2,DELIMITER,c3)

    except KeyboardInterrupt:
        pass
    finally:
        dcs.set_power_off()

if __name__ == '__main__':
    color_sensor=bh1745_driver()
    bus = open_bus_or_exit(color_sensor)
    test_data_logging(color_sensor)
    bus.close()

