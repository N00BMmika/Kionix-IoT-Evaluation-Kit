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
from lib.sensor_base import sensor_base

import bh1745_registers as sensor
r=sensor.registers()
b=sensor.bits()
m=sensor.masks()

class bh1745_driver(sensor_base):
    #Who am I
    _WAI =      ( b.BH1745_ID_REG_MANUFACTURER_ID )
    _WAIREG =   ( r.BH1745_ID_REG )
    _WAI2 =     ( b.BH1745_SYSTEM_CONTROL_PART_ID )
    _WAIREG2 =  ( r.BH1745_SYSTEM_CONTROL )

#Common mandatory functions
    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x38, 0x39]
        self.I2C_SUPPORT = True
        self.INT_PINS = [1]       #BH1745 has only one interrupt, but it can be connected to either of aardvark gpio pins.

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BH1745_REGISTER_DUMP_START, r.BH1745_REGISTER_DUMP_END)
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
        self.soft_reset()

    def ic_test(self):
        """ Read value, modify and write it back, read again. Make sure the value changed. Restore original value. """
         #ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BH1745_MODE_CONTROL1)[0]
        self.write_register(r.BH1745_MODE_CONTROL1, (datain1 ^ 0x01) )
        datain2 = self.read_register(r.BH1745_MODE_CONTROL1)[0]
        self.write_register(r.BH1745_MODE_CONTROL1, datain1)
        if datain2 == (datain1 ^ 0x01):
            return True
        return False

    def set_default_on(self):#
        """
        Setup sensor to be ready for multiple measurements
        """
        self.set_measurement_time(b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_160MSEC)
        self.set_adc_gain(b.BH1745_MODE_CONTROL2_ADC_GAIN_1X)
        self.disable_interrupt_latch()
        self.disable_int_pin()
        self.start_measurement()
        return

    def read_data(self):
        """
        :return: (uint16,uin16,uin16,uin16) raw data from (R,G,B,C)
        """
        data = self.read_register(r.BH1745_RED_DATA_LSBS, (2*4) )
        dataout = struct.unpack('HHHH',data)
        return dataout

#Common optional functions - power commands
    def set_power_on(self):
        self.start_measurement()                #component powers on when measurement is started.
        return

    def set_power_off(self):
        self.stop_measurement()                 #power down measurement block
        self.disable_int_pin()
        self.disable_int_pin_active_state()       #int pin keeps previous state on power off so set it to high impedance state to save power (25uA@2.5V)

        #self.soft_reset()
        return

    def soft_reset(self):   #aka old por()
        """
        All registers are reset and BH1745NUC becomes power down.
        """
        self.set_bit_pattern(r.BH1745_MODE_CONTROL1, b.BH1745_SYSTEM_CONTROL_SW_RESET_START, m.BH1745_SYSTEM_CONTROL_SW_RESET_MASK)
        return

    def get_soft_reset_state(self):
        """
        :return:  BH1745_SYSTEM_CONTROL_SW_RESET_NOT_STARTED / BH1745_SYSTEM_CONTROL_SW_RESET_START
        """
        initial_reset_state = self.read_register(r.BH1745_MODE_CONTROL1) & m.BH1745_SYSTEM_CONTROL_SW_RESET_MASK
        return initial_reset_state


#Common optional functions - power/hw setup
    def whoami(self):
        """
        :return: Get manufacturer ID
        """
        manufacturer_id = self.read_register(r.BH1745_ID_REG)[0]
        return manufacturer_id

    def is_int_pin_active_state_enabled(self):
        """
        :return: True/False
        """
        setup_phy_int_pin = self.read_register(r.BH1745_MODE_CONTROL1)[0] & m.BH1745_SYSTEM_CONTROL_INT_PIN_MASK

        if setup_phy_int_pin == b.BH1745_SYSTEM_CONTROL_INT_PIN_ACTIVE:
            return True
        elif setup_phy_int_pin == b.BH1745_SYSTEM_CONTROL_INT_PIN_INACTIVE:
            return False
        else:
            logger.debug('read error on setup phy int pin active/inactive')
            raise Exception
        #returned already

    def disable_int_pin_active_state(self):
        """
        INT pin to inactive, high impedance state
        """
        self.set_bit_pattern(r.BH1745_MODE_CONTROL1, b.BH1745_SYSTEM_CONTROL_INT_PIN_INACTIVE, m.BH1745_SYSTEM_CONTROL_INT_PIN_MASK)
        return

    def enable_int_pin_active_state(self):
        self.set_bit_pattern(r.BH1745_MODE_CONTROL1, b.BH1745_SYSTEM_CONTROL_INT_PIN_ACTIVE, m.BH1745_SYSTEM_CONTROL_INT_PIN_MASK)
        return

    def is_int_pin_enabled(self):
        """
        :return: True/False
        """
        status = self.read_register(r.BH1745_INTERRUPT)[0] & m.BH1745_INTERRUPT_PIN_MASK
        if status == b.BH1745_INTERRUPT_PIN_ENABLE:
            return True
        elif status == b.BH1745_INTERRUPT_PIN_DISABLE:
            return False
        else:
            logger.debug('read error on int pin disabled/enabled')
            raise Exception
        #returned already

    def enable_int_pin(self, intpin=1):
        assert intpin in self.INT_PINS
        self.set_bit_pattern(r.BH1745_INTERRUPT, b.BH1745_INTERRUPT_PIN_ENABLE, m.BH1745_INTERRUPT_PIN_MASK)
        return

    def disable_int_pin(self, intpin=1):
        assert intpin in self.INT_PINS
        self.set_bit_pattern(r.BH1745_INTERRUPT, b.BH1745_INTERRUPT_PIN_DISABLE, m.BH1745_INTERRUPT_PIN_MASK)
        return

    def is_drdy_pin_enabled(self):
        logger.debug('No drdy pin in BH1745.')
        return
    def enable_drdy_pin(self):
        logger.debug('No drdy pin in BH1745.')
        return
    def disable_drdy_pin(self):
        logger.debug('No drdy pin in BH1745.')
        return


#Sensor specific functions - measurement setup
    def get_measurement_time(self):
        time = self.read_register(r.BH1745_MODE_CONTROL1)[0] & m.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_MASK
        return time

    def set_measurement_time(self, time):
        """
        :param time: Exposure time as in BH1745_MODE_CONTROL1_MEASUREMENT_TIME_*
        """
        assert (time) in [  b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_160MSEC,    \
                            b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_320MSEC,    \
                            b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_640MSEC,    \
                            b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_1280MSEC,   \
                            b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_2560MSEC,   \
                            b.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_5120MSEC]
        self.set_bit_pattern(r.BH1745_MODE_CONTROL1, time, m.BH1745_MODE_CONTROL1_MEASUREMENT_TIME_MASK)
        return

    def get_adc_gain(self):
        """
        :return: b.BH1745_MODE_CONTROL2_ADC_GAIN_*
        """
        adc_gain = self.read_register(r.BH1745_MODE_CONTROL2)[0] & m.BH1745_MODE_CONTROL2_ADC_GAIN_MASK
        return adc_gain

    def set_adc_gain(self, gain):
        """
        :param gain: b.BH1745_MODE_CONTROL2_ADC_GAIN_*
        """
        assert (gain) in [  b.BH1745_MODE_CONTROL2_ADC_GAIN_1X,    \
                            b.BH1745_MODE_CONTROL2_ADC_GAIN_2X,    \
                            b.BH1745_MODE_CONTROL2_ADC_GAIN_16X]
        self.set_bit_pattern(r.BH1745_MODE_CONTROL2, gain, m.BH1745_MODE_CONTROL2_ADC_GAIN_MASK)

    def write_mode_control3(self):
        """
        Specification says to write 02h to this register, por default is 00h.
        """
        self.write_register(r.BH1745_MODE_CONTROL3, b.BH1745_MODE_CONTROL3_ALWAYS_02H)
        return

    def read_dint_data(self):
        """
        :return: (uint16) raw data from DINT test register
        """
        data = self.read_register(r.BH1745_DINT_DATA_LSBS, (2*1) )
        dataout = struct.unpack('H',data)
        return dataout

    def read_interrupt_tresholds(self):
        """
        :return: (uint16, uin16) raw data from (treshold_high, treshold_low)
        """
        data = self.read_register(r.BH1745_TH_LSBS, (2*2) )
        treshold_high, treshold_low = struct.unpack('HH',data)
        return treshold_high, treshold_low

    def write_interrupt_tresholds(self, treshold_low, treshold_high):
        if not ((0 <= treshold_high) and (treshold_high < 2**16)):
            logger.debug("treshold_high value out of bounds.")
            raise TypeError
        if not ((0 <= treshold_low) and (treshold_low < 2**16)):
            logger.debug("treshold_low value out of bounds.")
            raise TypeError
        THL = ( treshold_high        & 0xff )
        THH = ( treshold_high >> 8 ) & 0xff
        TLL = ( treshold_low         & 0xff )
        TLH = ( treshold_low  >> 8 ) & 0xff
        self.write_register(r.BH1745_TH_LSBS, THL)
        self.write_register(r.BH1745_TH_MSBS, THH)
        self.write_register(r.BH1745_TL_LSBS, TLL)
        self.write_register(r.BH1745_TL_MSBS, TLH)
        return

    def get_interrupt_persistence(self):
        """
        :return: b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function status
        """
        status = self.read_register(r.BH1745_PERSISTENCE)[0] & m.BH1745_PERSISTENCE_OF_INTERRUPT_MASK
        return status

    def set_interrupt_persistence(self, persistence):
        """
        :parameter: b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function
        """
        assert (persistence) in [   b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_TOGGLE_AFTER_MEASUREMENT,  \
                                    b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_MEASUREMENT,  \
                                    b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_4_SAME,       \
                                    b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_8_SAME]
        self.set_bit_pattern(r.BH1745_PERSISTENCE, persistence, m.BH1745_PERSISTENCE_OF_INTERRUPT_MASK)
        return

    def get_interrupt_source_channel(self):
        """
        :return: BH1745_INTERRUPT_SOURCE_*
        """
        channel = self.read_register(r.BH1745_INTERRUPT)[0] & m.BH1745_INTERRUPT_SOURCE_MASK
        return channel

    def set_interrupt_source_channel(self, channel):
        """
        :param channel: BH1745_INTERRUPT_SOURCE_*
        """
        assert (channel) in [   b.BH1745_INTERRUPT_SOURCE_SELECT_RED,   \
                                b.BH1745_INTERRUPT_SOURCE_SELECT_GREEN, \
                                b.BH1745_INTERRUPT_SOURCE_SELECT_BLUE,  \
                                b.BH1745_INTERRUPT_SOURCE_SELECT_CLEAR]
        self.set_bit_pattern(r.BH1745_INTERRUPT, channel, m.BH1745_INTERRUPT_LATCH_MASK)
        return

    def is_interrupt_latch_enabled(self):
        """
        :return: True : INT pin is latched until INTERRUPT register is read or initialized.
                 False: INT pin is updated after each measurement.
        """
        status = self.read_register(r.BH1745_INTERRUPT)[0] & m.BH1745_INTERRUPT_LATCH_MASK
        if   ( status == b.BH1745_INTERRUPT_LATCH_ENABLE  ):
            return True
        elif ( status == b.BH1745_INTERRUPT_LATCH_DISABLE ):
            return False
        else:
            logger.debug('read error on int latch enable/disable')
            raise Exception
        #should be returned already

    def enable_interrupt_latch(self):
        """
        INT pin is latched until INTERRUPT register is read or initialized.
        """
        self.set_bit_pattern(r.BH1745_INTERRUPT, b.BH1745_INTERRUPT_LATCH_ENABLE, m.BH1745_INTERRUPT_LATCH_MASK)
        return

    def disable_interrupt_latch(self):
        """
        INT pin is updated after each measurement.
        """
        self.set_bit_pattern(r.BH1745_INTERRUPT, b.BH1745_INTERRUPT_LATCH_DISABLE, m.BH1745_INTERRUPT_LATCH_MASK)
        return


#Common optional functions - measurement commands
    def start_measurement(self):
        """
        Write 1 to RGBC_EN.
        """
        self.set_bit_pattern(r.BH1745_MODE_CONTROL2, b.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_ACTIVE, m.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_MASK)
        return

    def stop_measurement(self):
        """
        Write 0 to RGBC_EN.
        """
        self.set_bit_pattern(r.BH1745_MODE_CONTROL2, b.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_INACTIVE, m.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_MASK)
        return

    def read_drdy(self):    #fixme: refactor top
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        reads VALID-register to see if new data is available
        :return: True/False
        """
        drdy = self.read_register(r.BH1745_MODE_CONTROL2)[0] & m.BH1745_MODE_CONTROL2_DATA_UPDATED_MASK
        if (drdy == b.BH1745_MODE_CONTROL2_DATA_UPDATED_YES):
            return True
        #else:
        return False

    def read_int_reg(self):
        """
        :return: r.BH1745_INTERRUPT_STATUS_*
        """
        status = self.read_register(r.BH1745_INTERRUPT)[0] & m.BH1745_INTERRUPT_STATUS_MASK
        return status

    def clear_interrupt(self):
        self.read_int_reg()
        return
