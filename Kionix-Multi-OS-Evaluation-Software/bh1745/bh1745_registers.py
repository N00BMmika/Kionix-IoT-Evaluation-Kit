# The MIT License (MIT)
# Copyright (c) 2017 Rohm Semiconductor
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
class register_base: pass
class registers(register_base):
	def __init__(self):
		self.BH1745_REGISTER_DUMP_START                           = 0x40         
		self.BH1745_SYSTEM_CONTROL                                = 0x40         
		self.BH1745_MODE_CONTROL1                                 = 0x41         # Writing MODE_CONTROL1/2/3 restarts measurement if any.
		self.BH1745_MODE_CONTROL2                                 = 0x42         
		self.BH1745_MODE_CONTROL3                                 = 0x44         # Always write 02h
		self.BH1745_RED_DATA_LSBS                                 = 0x50         # Least significant byte of uint16 RED measurement value
		self.BH1745_RED_DATA_MSBS                                 = 0x51         # Most significant byte of uint16 RED measurement value
		self.BH1745_GREEN_DATA_LSBS                               = 0x52         
		self.BH1745_GREEN_DATA_MSBS                               = 0x53         
		self.BH1745_BLUE_DATA_LSBS                                = 0x54         
		self.BH1745_BLUE_DATA_MSBS                                = 0x55         
		self.BH1745_CLEAR_DATA_LSBS                               = 0x56         
		self.BH1745_CLEAR_DATA_MSBS                               = 0x57         
		self.BH1745_DINT_DATA_LSBS                                = 0x58         # DINT data is used for internal calculation of BH1745NUC.
		self.BH1745_DINT_DATA_MSBS                                = 0x59         # DINT registers are used for IC test only.
		self.BH1745_INTERRUPT                                     = 0x60         
		self.BH1745_PERSISTENCE                                   = 0x61         
		self.BH1745_TH_LSBS                                       = 0x62         
		self.BH1745_TH_MSBS                                       = 0x63         
		self.BH1745_TL_LSBS                                       = 0x64         
		self.BH1745_TL_MSBS                                       = 0x65         
		self.BH1745_ID_REG                                        = 0x92         
		self.BH1745_REGISTER_DUMP_END                             = 0x92         
class bits(register_base):
	def __init__(self):
		self.BH1745_SYSTEM_CONTROL_SW_RESET_NOT_STARTED           = (0x00 << 7)  # Initial reset is not started
		self.BH1745_SYSTEM_CONTROL_SW_RESET_START                 = (0x01 << 7)  # Initial reset is started
		self.BH1745_SYSTEM_CONTROL_INT_PIN_ACTIVE                 = (0x00 << 6)  # In specification "not_initialized"
		self.BH1745_SYSTEM_CONTROL_INT_PIN_INACTIVE               = (0x01 << 6)  # high impedance
		self.BH1745_SYSTEM_CONTROL_PART_ID                        = (0x0B << 0)  
		self.BH1745_MODE_CONTROL1_RESERVED_WRITE00000             = (0x00 << 3)  
		self.BH1745_MODE_CONTROL1_ODR_6P25                        = (0x00 << 0)  # 160msec
		self.BH1745_MODE_CONTROL1_ODR_3P125                       = (0x01 << 0)  # 320msec
		self.BH1745_MODE_CONTROL1_ODR_1P5625                      = (0x02 << 0)  # 640msec
		self.BH1745_MODE_CONTROL1_ODR_0P78125                     = (0x03 << 0)  # 1280msec
		self.BH1745_MODE_CONTROL1_ODR_0P390625                    = (0x04 << 0)  # 2560msec
		self.BH1745_MODE_CONTROL1_ODR_0P1953125                   = (0x05 << 0)  # 5120msec
		self.BH1745_MODE_CONTROL1_ODR_FORBIDDEN6                  = (0x06 << 0)  # forbidden6
		self.BH1745_MODE_CONTROL1_ODR_FORBIDDEN7                  = (0x07 << 0)  # forbidden7
		self.BH1745_MODE_CONTROL2_DATA_UPDATED_NO                 = (0x00 << 7)  
		self.BH1745_MODE_CONTROL2_DATA_UPDATED_YES                = (0x01 << 7)  
		self.BH1745_MODE_CONTROL2_RESERVED65_WRITE00              = (0x00 << 5)  
		self.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_INACTIVE       = (0x00 << 4)  
		self.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_ACTIVE         = (0x01 << 4)  
		self.BH1745_MODE_CONTROL2_RESERVED32_WRITE00              = (0x00 << 2)  
		self.BH1745_MODE_CONTROL2_ADC_GAIN_1X                     = (0x00 << 0)  
		self.BH1745_MODE_CONTROL2_ADC_GAIN_2X                     = (0x01 << 0)  
		self.BH1745_MODE_CONTROL2_ADC_GAIN_16X                    = (0x02 << 0)  
		self.BH1745_MODE_CONTROL2_ADC_GAIN_FORBIDDEN3             = (0x03 << 0)  
		self.BH1745_MODE_CONTROL3_ALWAYS_02H                      = (0x02 << 0)  
		self.BH1745_INTERRUPT_STATUS_INACTIVE                     = (0x00 << 7)  
		self.BH1745_INTERRUPT_STATUS_ACTIVE                       = (0x01 << 7)  
		self.BH1745_INTERRUPT_RESERVED65_WRITE00                  = (0x00 << 5)  
		self.BH1745_INTERRUPT_LATCH_ENABLE                        = (0x00 << 4)  # INT pin is latched until INTERRUPT register is read or initialized
		self.BH1745_INTERRUPT_LATCH_DISABLE                       = (0x01 << 4)  # INT pin is updated after each measurement
		self.BH1745_INTERRUPT_SOURCE_SELECT_RED                   = (0x00 << 2)  # red channel
		self.BH1745_INTERRUPT_SOURCE_SELECT_GREEN                 = (0x01 << 2)  # green channel
		self.BH1745_INTERRUPT_SOURCE_SELECT_BLUE                  = (0x02 << 2)  # blue channel
		self.BH1745_INTERRUPT_SOURCE_SELECT_CLEAR                 = (0x03 << 2)  # clear channel
		self.BH1745_INTERRUPT_RESERVED1_WRITE0                    = (0x00 << 1)  
		self.BH1745_INTERRUPT_PIN_DISABLE                         = (0x00 << 0)  
		self.BH1745_INTERRUPT_PIN_ENABLE                          = (0x01 << 0)  
		self.BH1745_PERSISTENCE_RESERVED72_WRITE000000            = (0x00 << 2)  
		self.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_TOGGLE_AFTER_MEASUREMENT = (0x00 << 0)  # Interrupt status is toggled at each measurement end.
		self.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_MEASUREMENT = (0x01 << 0)  # Interrupt status is updated at each measurement end.
		self.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_4_SAME = (0x02 << 0)  # Interrupt status is updated if 4 consecutive threshold judgements are the same
		self.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_8_SAME = (0x03 << 0)  # Interrupt status is updated if 8 consecutive threshold judgements are the same
		self.BH1745_ID_REG_MANUFACTURER_ID                        = (0xE0 << 0)  
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1745_INTERRUPT_LATCH={
			'enable':_b.BH1745_INTERRUPT_LATCH_ENABLE,
			'disable':_b.BH1745_INTERRUPT_LATCH_DISABLE,
		}
		self.BH1745_PERSISTENCE_OF_INTERRUPT={
			'status_update_after_4_same':_b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_4_SAME,
			'status_toggle_after_measurement':_b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_TOGGLE_AFTER_MEASUREMENT,
			'status_update_after_measurement':_b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_MEASUREMENT,
			'status_update_after_8_same':_b.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_UPDATE_AFTER_8_SAME,
		}
		self.BH1745_INTERRUPT_SOURCE={
			'select_green':_b.BH1745_INTERRUPT_SOURCE_SELECT_GREEN,
			'select_clear':_b.BH1745_INTERRUPT_SOURCE_SELECT_CLEAR,
			'select_blue':_b.BH1745_INTERRUPT_SOURCE_SELECT_BLUE,
			'select_red':_b.BH1745_INTERRUPT_SOURCE_SELECT_RED,
		}
		self.BH1745_MODE_CONTROL2_DATA_UPDATED={
			'yes':_b.BH1745_MODE_CONTROL2_DATA_UPDATED_YES,
			'no':_b.BH1745_MODE_CONTROL2_DATA_UPDATED_NO,
		}
		self.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT={
			'active':_b.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_ACTIVE,
			'inactive':_b.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_INACTIVE,
		}
		self.BH1745_MODE_CONTROL2_ADC_GAIN={
			'forbidden3':_b.BH1745_MODE_CONTROL2_ADC_GAIN_FORBIDDEN3,
			'1x':_b.BH1745_MODE_CONTROL2_ADC_GAIN_1X,
			'2x':_b.BH1745_MODE_CONTROL2_ADC_GAIN_2X,
			'16x':_b.BH1745_MODE_CONTROL2_ADC_GAIN_16X,
		}
		self.BH1745_MODE_CONTROL1_ODR={
			'0p1953125':_b.BH1745_MODE_CONTROL1_ODR_0P1953125,
			'1p5625':_b.BH1745_MODE_CONTROL1_ODR_1P5625,
			'0p78125':_b.BH1745_MODE_CONTROL1_ODR_0P78125,
			'3p125':_b.BH1745_MODE_CONTROL1_ODR_3P125,
			'forbidden6':_b.BH1745_MODE_CONTROL1_ODR_FORBIDDEN6,
			'forbidden7':_b.BH1745_MODE_CONTROL1_ODR_FORBIDDEN7,
			'6p25':_b.BH1745_MODE_CONTROL1_ODR_6P25,
			'0p390625':_b.BH1745_MODE_CONTROL1_ODR_0P390625,
		}
		self.BH1745_INTERRUPT_PIN={
			'enable':_b.BH1745_INTERRUPT_PIN_ENABLE,
			'disable':_b.BH1745_INTERRUPT_PIN_DISABLE,
		}
		self.BH1745_SYSTEM_CONTROL_SW_RESET={
			'start':_b.BH1745_SYSTEM_CONTROL_SW_RESET_START,
			'not_started':_b.BH1745_SYSTEM_CONTROL_SW_RESET_NOT_STARTED,
		}
		self.BH1745_SYSTEM_CONTROL_INT_PIN={
			'active':_b.BH1745_SYSTEM_CONTROL_INT_PIN_ACTIVE,
			'inactive':_b.BH1745_SYSTEM_CONTROL_INT_PIN_INACTIVE,
		}
		self.BH1745_INTERRUPT_STATUS={
			'active':_b.BH1745_INTERRUPT_STATUS_ACTIVE,
			'inactive':_b.BH1745_INTERRUPT_STATUS_INACTIVE,
		}
class masks(register_base):
	def __init__(self):
		self.BH1745_SYSTEM_CONTROL_SW_RESET_MASK                  = 0x80         # In specification named as SW_RESET
		self.BH1745_SYSTEM_CONTROL_INT_PIN_MASK                   = 0x40         
		self.BH1745_SYSTEM_CONTROL_PART_MASK                      = 0x3F         
		self.BH1745_MODE_CONTROL1_RESERVED_MASK                   = 0xF8         
		self.BH1745_MODE_CONTROL1_ODR_MASK                        = 0x07         
		self.BH1745_MODE_CONTROL2_DATA_UPDATED_MASK               = 0x80         # Is the RGBC data updated after last MODE_CONTROL1/2 reg writing or MODE_CONTROL2 reading. In specification named as VALID.
		self.BH1745_MODE_CONTROL2_RESERVED65_MASK                 = 0x60         # write 00
		self.BH1745_MODE_CONTROL2_RGBC_MEASUREMENT_MASK           = 0x10         # In specification named as RGBC_EN
		self.BH1745_MODE_CONTROL2_RESERVED32_MASK                 = 0x0C         # write 00
		self.BH1745_MODE_CONTROL2_ADC_GAIN_MASK                   = 0x03         # RGBC measurement ADC gain (multiplier)
		self.BH1745_MODE_CONTROL3_ALWAYS_MASK                     = 0xFF         
		self.BH1745_INTERRUPT_STATUS_MASK                         = 0x80         # INT status of RGBC (read only)
		self.BH1745_INTERRUPT_RESERVED65_MASK                     = 0x60         
		self.BH1745_INTERRUPT_LATCH_MASK                          = 0x10         # In specification named as INT LATCH
		self.BH1745_INTERRUPT_SOURCE_MASK                         = 0x0C         
		self.BH1745_INTERRUPT_RESERVED1_MASK                      = 0x02         # Write 0
		self.BH1745_INTERRUPT_PIN_MASK                            = 0x01         # In specification named as INT ENABLE
		self.BH1745_PERSISTENCE_RESERVED72_MASK                   = 0xFC         
		self.BH1745_PERSISTENCE_OF_INTERRUPT_MASK                 = 0x03         # In specification named as PERSISTENCE
		self.BH1745_ID_REG_MANUFACTURER_MASK                      = 0xFF         