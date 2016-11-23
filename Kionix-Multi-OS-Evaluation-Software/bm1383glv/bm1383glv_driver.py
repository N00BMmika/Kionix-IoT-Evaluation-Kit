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

import bm1383glv_registers as sensor
r=sensor.registers()
b=sensor.bits()
m=sensor.masks()

class bm1383glv_driver(sensor_base):
    _WAI = ( b.BM1383GLV_ID_REG_MANUFACTURER_ID | b.BM1383GLV_ID_REG_PART_ID )
    _WAIREG = r.BM1383GLV_ID_REG

    def __init__(self):
        sensor_base.__init__(self)
        self.I2C_SAD_LIST = [0x5d]
        self.I2C_SUPPORT = True
        self.INT_PINS = [1,2]

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BM1383GLV_REGISTER_DUMP_START, r.BM1383GLV_REGISTER_DUMP_END)
        return

    def probe(self):
        """
        Read component ID and compare it to expected value.
        :return: True,  component is found.
                 False, component is not found
        """
        resp = self.read_register(self._WAIREG)
        if resp[0] == self._WAI:
            return 1
        return 0
        
    def ic_test(self):
        """
        Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
        ic should be powered on before trying this, otherwise it will fail.
        """
        datain1 = self.read_register(r.BM1383GLV_INT_LOW_TRESHOLD_LSB)[0]
        self.write_register(r.BM1383GLV_INT_LOW_TRESHOLD_LSB, (~datain1 & 0xff) )
        datain2 = self.read_register(r.BM1383GLV_INT_LOW_TRESHOLD_LSB)[0]
        self.write_register(r.BM1383GLV_INT_LOW_TRESHOLD_LSB, datain1)
        if datain2 == (~datain1 & 0xff):
            return True
        return False

    def por(self):  
        """
        Initiate soft reset.
        """
        self.set_power_on()     #reset control register is not active is power is off
        self.write_register(r.BM1383GLV_RESET_CONTROL_REG, b.BM1383GLV_RESET_CONTROL_REG_SW_RESET_EXECUTE)
        delay_seconds(20 / 1000.) # 20ms startup delay
        
    def set_default_on(self):
        """
        Setup sensor to be ready for multiple measurements
        """
        self.set_power_on()
        self.set_odr(b.BM1383GLV_MODE_CONTROL_REG_MODE_100MS)
        self.set_averaging(b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_SINGLE)
        return

    def read_data(self):
        #return self.read_data_raw()
        return self.read_temperature_pressure()        #Choose between these two outputs for default
        
    def set_power_on(self): 
        self.write_register(r.BM1383GLV_POWER_REG, b.BM1383GLV_POWER_REG_POWER_UP)
        self.write_register(r.BM1383GLV_SLEEP_REG, b.BM1383GLV_SLEEP_REG_SLEEP_OFF)
        return
        
    def set_power_off(self):
        self.write_register(r.BM1383GLV_SLEEP_REG, b.BM1383GLV_SLEEP_REG_SLEEP_ON)
        self.write_register(r.BM1383GLV_POWER_REG, b.BM1383GLV_POWER_REG_POWER_DOWN)
        return

    def read_data_raw(self):
        data = self.read_register(r.BM1383GLV_TEMPERATURE_OUT_MSB,5)
        dataout = struct.unpack('BBBBB',data)
        return dataout

    def read_temperature_pressure(self):
        data = self.read_register(r.BM1383GLV_TEMPERATURE_OUT_MSB,5)

        (T_raw, P_raw, P_raw_xlb) = struct.unpack('>hHB',data)
        temperatureC = float( T_raw ) / 32      #'C
        P_all = ( P_raw << 6 )  |  ( P_raw_xlb & 0b00111111 )
        pressure_hPa = float( P_all ) / 2048    #hPa

        return temperatureC, pressure_hPa       #Temp 'C, Pressure hPa   (10hPa = 1kPa)

    def read_temperature(self):
        data = self.read_register(r.BM1383GLV_TEMPERATURE_OUT_MSB,2)
        T_raw = struct.unpack('>h',data)
        temperatureC = float( T_raw ) / 32      #'C
        return temperatureC                     #Temp 'C, Pressure hPa   (10hPa = 1kPa)

    def read_pressure(self):
        data = self.read_register(r.BM1383GLV_PRESSURE_OUT_MSB,3)
        (P_raw, P_raw_xlb) = struct.unpack('>HB',data)
        P_all = ( P_raw << 6 )  |  ( P_raw_xlb & 0b00111111 )
        pressure_hPa = float( P_all ) / 2048    #hPa
        return pressure_hPa       #Temp 'C, Pressure hPa   (10hPa = 1kPa)


    def set_odr(self, mode):
        """
        :param mode: b.BM1383GLV_MODE_CONTROL_REG_MODE_*
        """
        assert ( mode ) in [    b.BM1383GLV_MODE_CONTROL_REG_MODE_STANDBY, \
                            b.BM1383GLV_MODE_CONTROL_REG_MODE_ONE_SHOT,\
                            b.BM1383GLV_MODE_CONTROL_REG_MODE_50MS,    \
                            b.BM1383GLV_MODE_CONTROL_REG_MODE_100MS,   \
                            b.BM1383GLV_MODE_CONTROL_REG_MODE_200MS ]
        self.set_bit_pattern(r.BM1383GLV_MODE_CONTROL_REG, mode, m.BM1383GLV_MODE_CONTROL_REG_MODE_MASK)

        inreg = self.read_odr()
        if ( inreg != mode ):
            logger.debug('set_odf failed')
        return

    def read_odr(self):
        sampling_mode = self.read_register(r.BM1383GLV_MODE_CONTROL_REG)[0] & m.BM1383GLV_MODE_CONTROL_REG_MODE_MASK
        return sampling_mode

    #input ave_num is b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_*
    def set_averaging(self, ave_num):
        """
        :param ave_num: b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_*
        """
        assert (ave_num) in [b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_SINGLE,   \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_2_TIMES,  \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_4_TIMES,  \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_8_TIMES,  \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_16_TIMES, \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_32_TIMES, \
                            b.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_64_TIMES]            
        self.set_bit_pattern(r.BM1383GLV_MODE_CONTROL_REG, ave_num, m.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_MASK)
        return

    def set_pressure_int_upper_treshold_raw(self, pressure_raw):
        """
        Sets upper treshold for high interrupt. Input value should be uint16
        """

        if (( 0 <= pressure_raw ) and ( pressure_raw < 2**16) ):
            tmp_MSB = ( pressure_raw & 0xff00 ) >> 8
            tmp_LSB = ( pressure_raw & 0xff )
            self.write_register(r.BM1383GLV_INT_HIGH_TRESHOLD_MSB, tmp_MSB)
            self.write_register(r.BM1383GLV_INT_HIGH_TRESHOLD_LSB, tmp_LSB)
        else:
            logger.debug('Pressure int high treshold value out of uint16.')
        return

    def set_pressure_int_lower_treshold_raw(self, pressure_raw):
        """
        Sets lower treshold for high interrupt. Input value should be uint16
        """
        if (0 <= pressure_raw and pressure_raw < 2**16):
            tmp_MSB = ( pressure_raw & 0xff00 ) >> 8
            tmp_LSB = ( pressure_raw & 0xff )
            self.write_register(r.BM1383GLV_INT_LOW_TRESHOLD_MSB, tmp_MSB)
            self.write_register(r.BM1383GLV_INT_LOW_TRESHOLD_LSB, tmp_LSB)
        else:
            logger.debug('Pressure int low treshold value out of uint16.')
        return

    def enable_pressure_treshold_interrupts(self):
        """
        Enables both higher and lower treshold interrupt.
        """
        self.enable_pressure_low_treshold_interrupt()
        self.enable_pressure_high_treshold_interrupt()
        self.enable_pressure_interrupt_main()
        return

    def enable_pressure_interrupt_main(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INTERRUPT_ENABLE, m.BM1383GLV_INT_CONTROL_REG_INTERRUPT_MASK)
        return

    def enable_pressure_low_treshold_interrupt(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_LOW_ENABLE, m.BM1383GLV_INT_CONTROL_REG_INT_LOW_MASK)
        return

    def enable_pressure_high_treshold_interrupt(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_HIGH_ENABLE, m.BM1383GLV_INT_CONTROL_REG_INT_HIGH_MASK)
        return

    def disable_pressure_treshold_interrupts(self):
        """
        Disables both higher and lower treshold interrupt.
        """
        self.disable_pressure_low_treshold_interrupt()
        self.disable_pressure_high_treshold_interrupt()
        self.disable_pressure_interrupt_main()
        return

    def disable_pressure_interrupt_main(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INTERRUPT_DISABLE, m.BM1383GLV_INT_CONTROL_REG_INTERRUPT_MASK)
        return

    def disable_pressure_low_treshold_interrupt(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_LOW_DISABLE, m.BM1383GLV_INT_CONTROL_REG_INT_LOW_MASK)
        return

    def disable_pressure_high_treshold_interrupt(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_HIGH_DISABLE, m.BM1383GLV_INT_CONTROL_REG_INT_HIGH_MASK)
        return

    def enable_pressure_interrupt_pin_pullup(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_ENABLE, m.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_MASK)
        return

    def disable_pressure_interrupt_pin_pullup(self):
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_DISABLE, m.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_MASK)
        return

    def enable_pressure_interrupt_latching(self):
        """ Keep interrupt until cleared """
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_KEEP_UNTIL_CLEARED, m.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_MASK)
        return

    def disable_pressure_interrupt_latching(self):
        """ Update interrupt status after every measurement, regardless of reading/clearing. """
        self.set_bit_pattern(r.BM1383GLV_INT_CONTROL_REG, b.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_CONTINUOUS_UPDATE, m.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_MASK)
        return

    def is_interrupt_triggered(self):
        """ Read interrupt status register, return value "is interrupt triggered" True/False """
        return ( self.read_register( r.BM1383GLV_INT_CONTROL_REG )[0] & ( m.BM1383GLV_INT_CONTROL_REG_TRESHOLD_HIGH_MASK | m.BM1383GLV_INT_CONTROL_REG_TRESHOLD_LOW_MASK  ) != 0 )

    def read_drdy(self):
        """ used by framework. "Poll data ready register via i2c" """
        logger.info('read_drdy called, but bm1383glv does not provide drdy information')
        raise NotImplementedError

    def clear_interrupt(self):
            self.write_register(r.BM1383GLV_RESET_CONTROL_REG, b.BM1383GLV_RESET_CONTROL_REG_INT_RESET_INACTIVE )

