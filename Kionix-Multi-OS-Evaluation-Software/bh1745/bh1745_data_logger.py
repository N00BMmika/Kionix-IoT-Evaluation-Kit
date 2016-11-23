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
    Test data logging, using drdy polling setup from settings.cfg. All configuration options are listed in here before measurement block.
    """
    try:
        dcs.set_default_on()
        dcs.stop_measurement()

        status = dcs.ic_test()
        if (status != True):
            logger.debug("ic_test failed")

        #dcs.enable_int_pin_active_state()
        dcs.disable_int_pin_active_state()

        dcs.enable_int_pin()        #In range 2.5V, interrupted -> 0V
        #dcs.disable_int_pin()

        #Note: Measurement values are not comparable between different measurement times.
        # Longer measurement time yields greater result value.
        dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_160MSEC)
        #dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_320MSEC)
        #dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_640MSEC)
        #dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_1280MSEC)
        #dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_2560MSEC)
        #dcs.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_5120MSEC)

        dcs.set_adc_gain(b.BH1745_MODE_CONTROL2_ADC_GAIN_1X)
        #dcs.set_adc_gain(b.BH1745_MODE_CONTROL2_ADC_GAIN_2X)
        #dcs.set_adc_gain(b.BH1745_MODE_CONTROL2_ADC_GAIN_16X)

        #dcs.write_mode_control3()

        #dcs.write_interrupt_tresholds(0, ((2**16)-1) )  #never interrupt
        dcs.write_interrupt_tresholds(1, 0)             #always interrupt, kind of DRDY mode

        dcs.set_interrupt_persistence(b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_TOGGLE_AFTER_MEASUREMENT)
        #dcs.set_interrupt_persistence(b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_MEASUREMENT)
        #dcs.set_interrupt_persistence(b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_4_SAME)
        #dcs.set_interrupt_persistence(b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_8_SAME)

        dcs.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_RED)
        #dcs.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_GREEN)
        #dcs.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_BLUE)
        #dcs.set_interrupt_source_channel(b.BH1745_INTERRUPT_SOURCE_SELECT_CLEAR)

        dcs.enable_interrupt_latch()        #keep int until cleared
        #dcs.disable_interrupt_latch()

        dcs.start_measurement()

        now = timing.time_elapsed()
        print '%f%s%s%s%s%s%s%s%s' %  (now,DELIMITER,'     R',DELIMITER,'     G',DELIMITER,'     B',DELIMITER,'     C')

        while 1:
            dcs.drdy_function()            # follows the configuration from settings.cfg
            dcs.clear_interrupt()

            now = timing.time_elapsed()
            c0,c1,c2,c3 = dcs.read_data()
            print '%f%s%6.d%s%6.d%s%6.d%s%6.d' %  (now,DELIMITER,c0,DELIMITER,c1,DELIMITER,c2,DELIMITER,c3)

    except KeyboardInterrupt:
        pass
    finally:
        dcs.set_power_off()

if __name__ == '__main__':
    color_sensor=bh1745_driver()
    bus = open_bus_or_exit(color_sensor)
    test_data_logging(color_sensor)
    bus.close()

