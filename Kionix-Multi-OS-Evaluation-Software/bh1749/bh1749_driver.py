# The MIT License (MIT)
#
# Copyright (c) 2016 Rohm Semiconductor
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
"""
   Driver for BH1749 Color sensor
"""

import struct
import time
# from imports import *
from lib.util_lib import logger
from lib.sensor_base import sensor_base

import bh1749_registers as sensor
r = sensor.registers()
b = sensor.bits()
m = sensor.masks()
e = sensor.enums()


class bh1749_driver(sensor_base):
    """
    Class bh1749 defines sensor specific functionality
    """
    _WAI = (b.BH1749_ID_REG_MANUFACTURER_ID)
    _WAIREG = (r.BH1749_ID_REG)
    _WAI2 = (b.BH1749_SYSTEM_CONTROL_PART_ID)
    _WAIREG2 = (r.BH1749_SYSTEM_CONTROL)
    _WAIREG2MASK = (m.BH1749_SYSTEM_CONTROL_PART_MASK)

# Common mandatory functions
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x38, 0x39]
        self.I2C_SUPPORT = True

        """ BH1749 has only one interrupt, but it can be connected
            to either of aardvark gpio pins."""
        self.INT_PINS = [1]

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BH1749_REGISTER_DUMP_START,
                            r.BH1749_REGISTER_DUMP_END)
        return

    def probe(self):
        """
        Read component ID and compare it to expected value
        :return:    1 if component matches this driver,
                    0 if component doesn't match
        """

        resp = self.read_register(self._WAIREG)
        if resp[0] == self._WAI:
            resp = self.read_register(self._WAIREG2)
            if resp[0] == self._WAI2:
                return 1
        return 0

    def por(self):
        """
        Reset the chip
        """
        self.soft_reset()

    def set_power_off(self):
        self.soft_reset()

    def ic_test(self):
        """ Read value, modify and write it back, read again.
            Make sure the value changed. Restore original value.
        """
        # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BH1749_MODE_CONTROL1)[0]
        self.write_register(r.BH1749_MODE_CONTROL1, (datain1 ^ 0x8))
        datain2 = self.read_register(r.BH1749_MODE_CONTROL1)[0]
        self.write_register(r.BH1749_MODE_CONTROL1, datain1)
        self.soft_reset()
        if datain2 == (datain1 ^ 0x8):
            return True
        return False

    def set_default_on(self):
        """
        Setup sensor to be ready for multiple measurements
        this function is used by hello_sensor, needs a small delay
        before return to get the measurement done before reading
        """
        self.set_interrupt_persistence(
            b.BH1749_PERSISTENCE_MODE_STATUS_ACTIVE_AFTER_MEASUREMENT)
        self.enable_int_pin()
        self.start_measurement(b.BH1749_MODE_CONTROL1_ODR_28P6,
                               b.BH1749_MODE_CONTROL1_RGB_GAIN_1X,
                               b.BH1749_MODE_CONTROL1_IR_GAIN_1X)
        time.sleep(0.2)
        return

    def read_data(self):
        """
        :return: (uint16,uin16,uin16,uint16,uint16) raw data from (R,G,B,IR,G2)
        """
        rgb = self.read_register(r.BH1749_RED_DATA_LSBS, (2*3))
        dataout = struct.unpack('HHH', rgb)
        irg2 = self.read_register(r.BH1749_IR_DATA_LSBS, (2*2))
        dataout += struct.unpack('HH', irg2)
        return dataout

# Common optional functions - power commands
    def soft_reset(self):   # aka old por()
        """
        All registers are reset and BH1749NUC becomes power down.
        """
        self.set_bit_pattern(r.BH1749_SYSTEM_CONTROL,
                             b.BH1749_SYSTEM_CONTROL_SW_RESET_DONE,
                             m.BH1749_SYSTEM_CONTROL_SW_RESET_MASK)
        return

# Common optional functions - power/hw setup
    def whoami(self):
        """
        :return: Get manufacturer ID
        """
        manufacturer_id = self.read_register(r.BH1749_ID_REG)[0]
        return manufacturer_id

    def enable_int_pin(self, intpin=1):
        """
        Enable interrupt functionality
        """
        assert intpin in self.INT_PINS
        self.set_bit_pattern(r.BH1749_INTERRUPT, b.BH1749_INTERRUPT_EN_ENABLE,
                             m.BH1749_INTERRUPT_EN_MASK)
        return

    def disable_int_pin(self, intpin=1):
        """
        Disable interrupt functionality
        """
        assert intpin in self.INT_PINS
        self.set_bit_pattern(r.BH1749_INTERRUPT,
                             b.BH1749_INTERRUPT_EN_DISABLE,
                             m.BH1749_INTERRUPT_EN_MASK)
        return

# Sensor specific functions - measurement setup
    def _set_measurement_time(self, meas_time):
        """
        :param time: Exposure time as in BH1749_MODE_CONTROL1_ODR_*
        """
        assert meas_time in [b.BH1749_MODE_CONTROL1_ODR_28P6,
                             b.BH1749_MODE_CONTROL1_ODR_8P333,
                             b.BH1749_MODE_CONTROL1_ODR_4P167]
        self.set_bit_pattern(r.BH1749_MODE_CONTROL1, meas_time,
                             m.BH1749_MODE_CONTROL1_ODR_MASK)
        return

    def _set_rgb_gain(self, gain):
        """
        :param gain: b.BH1749_MODE_CONTROL1_RGB_GAIN_*
        """
        assert gain in [b.BH1749_MODE_CONTROL1_RGB_GAIN_1X,
                        b.BH1749_MODE_CONTROL1_RGB_GAIN_32X]

        self.set_bit_pattern(r.BH1749_MODE_CONTROL1, gain,
                             m.BH1749_MODE_CONTROL1_RGB_GAIN_MASK)

    def _set_ir_gain(self, gain):
        """
        :param gain: b.BH1749_MODE_CONTROL1_IR_GAIN_*
        """
        assert gain in [b.BH1749_MODE_CONTROL1_IR_GAIN_1X,
                        b.BH1749_MODE_CONTROL1_IR_GAIN_32X]

        self.set_bit_pattern(r.BH1749_MODE_CONTROL1, gain,
                             m.BH1749_MODE_CONTROL1_IR_GAIN_MASK)

    def write_interrupt_tresholds(self, treshold_low, treshold_high):
        """
        :param uint16 threshold_low, uint16 threshold_high
        """
        if not ((treshold_high >= 0) and (treshold_high < 2**16)):
            logger.debug("treshold_high value out of bounds.")
            raise TypeError
        if not ((treshold_low >= 0) and (treshold_low < 2**16)):
            logger.debug("treshold_low value out of bounds.")
            raise TypeError
        thl = (treshold_high & 0xff)
        thh = (treshold_high >> 8) & 0xff
        tll = (treshold_low & 0xff)
        tlh = (treshold_low >> 8) & 0xff
        self.write_register(r.BH1749_TH_LSBS, thl)
        self.write_register(r.BH1749_TH_MSBS, thh)
        self.write_register(r.BH1749_TL_LSBS, tll)
        self.write_register(r.BH1749_TL_MSBS, tlh)
        return

    def set_interrupt_persistence(self, psn):
        """
        :parameter: b.BH1749_PERSISTENCE_MODE Interrupt persistence function
        """
        assert psn in [
            b.BH1749_PERSISTENCE_MODE_STATUS_ACTIVE_AFTER_MEASUREMENT,
            b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_MEASUREMENT,
            b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_4_SAME,
            b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_8_SAME]
        self.set_bit_pattern(r.BH1749_PERSISTENCE, psn,
                             m.BH1749_PERSISTENCE_MODE_MASK)
        return

    def set_interrupt_source_channel(self, channel):
        """
        :param channel: BH1749_INTERRUPT_SOURCE_*
        """
        assert channel in [b.BH1749_INTERRUPT_SOURCE_SELECT_RED,
                           b.BH1749_INTERRUPT_SOURCE_SELECT_GREEN,
                           b.BH1749_INTERRUPT_SOURCE_SELECT_BLUE]
        self.set_bit_pattern(r.BH1749_INTERRUPT, channel,
                             m.BH1749_INTERRUPT_SOURCE_MASK)
        return

# Common optional functions - measurement commands
    def start_measurement(self,
                          measurement_time,
                          rgb_gain,
                          ir_gain):
        """
        Set measurement time and write 1 to RGB_EN.
        Measurement time, rgb gain and ir gain  are in forbidden value by
        default, so starting measurement is heavily coupled to these
        variables. This is the reason for haveing them as parameters.
        """
        self._set_measurement_time(measurement_time)
        self._set_rgb_gain(rgb_gain)
        self._set_ir_gain(ir_gain)
        self.set_bit_pattern(r.BH1749_MODE_CONTROL2,
                             b.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_ACTIVE,
                             m.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_MASK)
        return

    def stop_measurement(self):
        """
        Write 0 to RGB_EN.
        """
        self.set_bit_pattern(r.BH1749_MODE_CONTROL2,
                             b.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_INACTIVE,
                             m.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_MASK)
        self.clear_interrupt()
        return

    def read_drdy(self):
        """
        reads VALID-register to see if new data is available
        :return: True/False
        """
        drdy = self.read_register(r.BH1749_MODE_CONTROL2)[0] & \
            m.BH1749_MODE_CONTROL2_VALID_MASK
        if drdy == b.BH1749_MODE_CONTROL2_VALID_YES:
            return True
        return False

    def interrupt_status(self):
        """
        :return: r.BH1749_INTERRUPT_STATUS_*
        """
        status = self.read_register(r.BH1749_INTERRUPT)[0] & \
            m.BH1749_INTERRUPT_STATUS_MASK
        return status

    def clear_interrupt(self):
        """
        Clear interrupt status by reading interrupt status
        """
        self.interrupt_status()
        return
