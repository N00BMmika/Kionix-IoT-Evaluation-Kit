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
		self.RPR0521_REGISTER_DUMP_START                          = 0x40         
		self.RPR0521_SYSTEM_CONTROL                               = 0x40         
		self.RPR0521_MODE_CONTROL                                 = 0x41         
		self.RPR0521_ALS_PS_CONTROL                               = 0x42         
		self.RPR0521_PS_CONTROL                                   = 0x43         
		self.RPR0521_PS_DATA_LSBS                                 = 0x44         
		self.RPR0521_PS_DATA_MSBS                                 = 0x45         
		self.RPR0521_ALS_DATA0_LSBS                               = 0x46         
		self.RPR0521_ALS_DATA0_MSBS                               = 0x47         
		self.RPR0521_ALS_DATA1_LSBS                               = 0x48         
		self.RPR0521_ALS_DATA1_MSBS                               = 0x49         
		self.RPR0521_INTERRUPT                                    = 0x4A         
		self.RPR0521_PS_TH_LSBS                                   = 0x4B         # low 8bit
		self.RPR0521_PS_TH_MSBS                                   = 0x4C         # high 4bit
		self.RPR0521_PS_TL_LSBS                                   = 0x4D         # low 8bit
		self.RPR0521_PS_TL_MSBS                                   = 0x4E         # high 4bit
		self.RPR0521_ALS_DATA0_TH_LSBS                            = 0x4F         # low 8bit
		self.RPR0521_ALS_DATA0_TH_MSBS                            = 0x50         # high 8bit
		self.RPR0521_ALS_DATA0_TL_LSBS                            = 0x51         # low 8bit
		self.RPR0521_ALS_DATA0_TL_MSBS                            = 0x52         # high 8bit
		self.RPR0521_PS_OFFSET_LSBS                               = 0x53         # low 8bit
		self.RPR0521_PS_OFFSET_MSBS                               = 0x54         # high 2bit
		self.RPR0521_MANUFACT                                     = 0x92         
		self.RPR0521_REGISTER_DUMP_END                            = 0x54         
class bits(register_base):
	def __init__(self):
		self.RPR0521_SYSTEM_CONTROL_SW_RESET_NOT_STARTED          = (0x00 << 7)  
		self.RPR0521_SYSTEM_CONTROL_SW_RESET_START                = (0x01 << 7)  
		self.RPR0521_SYSTEM_CONTROL_INT_PIN_NO_INIT               = (0x00 << 6)  
		self.RPR0521_SYSTEM_CONTROL_INT_PIN_HI_Z                  = (0x01 << 6)  
		self.RPR0521_SYSTEM_CONTROL_PART_ID                       = (0x0A << 0)  
		self.RPR0521_MODE_CONTROL_ALS_EN_FALSE                    = (0x00 << 7)  
		self.RPR0521_MODE_CONTROL_ALS_EN_TRUE                     = (0x01 << 7)  
		self.RPR0521_MODE_CONTROL_PS_EN_FALSE                     = (0x00 << 6)  
		self.RPR0521_MODE_CONTROL_PS_EN_TRUE                      = (0x01 << 6)  
		self.RPR0521_MODE_CONTROL_PS_PULSE_200US                  = (0x00 << 5)  
		self.RPR0521_MODE_CONTROL_PS_PULSE_330US                  = (0x01 << 5)  
		self.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_NORMAL        = (0x00 << 4)  
		self.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT = (0x01 << 4)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF        = (0x00 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS       = (0x01 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS       = (0x02 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS      = (0x03 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS      = (0x04 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS     = (0x05 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS    = (0x06 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS    = (0x07 << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS     = (0x08 << 0)  # ALS measurement time is 100ms, sleep time is 300ms
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS    = (0x09 << 0)  # ALS measurement time is 100ms, sleep time is 300ms
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF      = (0x0A << 0)  # Measurement time 400ms, high sensitivity mode.
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS    = (0x0B << 0)  
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS      = (0x0C << 0)  # Additional sw process is necessary. Check P.18
		self.RPR0521_ALS_PS_CONTROL_RESERVED67_WRITE_00           = (0x00 << 6)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1             = (0x00 << 4)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2             = (0x01 << 4)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64            = (0x02 << 4)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128           = (0x03 << 4)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1             = (0x00 << 2)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2             = (0x01 << 2)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64            = (0x02 << 2)  
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128           = (0x03 << 2)  
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT_25MA              = (0x00 << 0)  
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT_50MA              = (0x01 << 0)  
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT_100MA             = (0x02 << 0)  
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT_200MA             = (0x03 << 0)  
		self.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_LOW               = (0x00 << 6)  
		self.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_HIGH              = (0x01 << 6)  
		self.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_TOO_HIGH          = (0x02 << 6)  
		self.RPR0521_PS_CONTROL_PS_GAIN_X1                        = (0x00 << 4)  
		self.RPR0521_PS_CONTROL_PS_GAIN_X2                        = (0x01 << 4)  
		self.RPR0521_PS_CONTROL_PS_GAIN_X4                        = (0x02 << 4)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_DRDY                  = (0x00 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1         = (0x01 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2         = (0x02 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3         = (0x03 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4         = (0x04 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5         = (0x05 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6         = (0x06 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7         = (0x07 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8         = (0x08 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9         = (0x09 << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10        = (0x0A << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11        = (0x0B << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12        = (0x0C << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13        = (0x0D << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14        = (0x0E << 0)  
		self.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15        = (0x0F << 0)  
		self.RPR0521_INTERRUPT_PS_INT_STATUS_INACTIVE             = (0x00 << 7)  
		self.RPR0521_INTERRUPT_PS_INT_STATUS_ACTIVE               = (0x01 << 7)  
		self.RPR0521_INTERRUPT_ALS_INT_STATUS_INACTIVE            = (0x00 << 6)  
		self.RPR0521_INTERRUPT_ALS_INT_STATUS_ACTIVE              = (0x01 << 6)  
		self.RPR0521_INTERRUPT_INT_MODE_PS_TH_H_ACTIVE            = (0x00 << 4)  
		self.RPR0521_INTERRUPT_INT_MODE_PS_TH_HYSTERESIS          = (0x01 << 4)  
		self.RPR0521_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION   = (0x02 << 4)  
		self.RPR0521_INTERRUPT_INT_MODE_FORBIDDEN                 = (0x03 << 4)  
		self.RPR0521_INTERRUPT_INT_ASSERT_STABLE                  = (0x00 << 3)  
		self.RPR0521_INTERRUPT_INT_ASSERT_REINT                   = (0x01 << 3)  
		self.RPR0521_INTERRUPT_INT_LATCH_ENABLED                  = (0x00 << 2)  
		self.RPR0521_INTERRUPT_INT_LATCH_DISABLED                 = (0x01 << 2)  
		self.RPR0521_INTERRUPT_INT_TRIG_INACTIVE                  = (0x00 << 0)  
		self.RPR0521_INTERRUPT_INT_TRIG_BY_PS                     = (0x01 << 0)  
		self.RPR0521_INTERRUPT_INT_TRIG_BY_ALS                    = (0x02 << 0)  
		self.RPR0521_INTERRUPT_INT_TRIG_BY_BOTH                   = (0x03 << 0)  
		self.RPR0521_MANUFACT_ID_E0H                              = (0xE0 << 0)  
_b=bits()
class enums(register_base):
	def __init__(self):
		self.RPR0521_INTERRUPT_ALS_INT_STATUS={
			'active':_b.RPR0521_INTERRUPT_ALS_INT_STATUS_ACTIVE,
			'inactive':_b.RPR0521_INTERRUPT_ALS_INT_STATUS_INACTIVE,
		}
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME={
			'400ms_400ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS,
			'400ms_100ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS,
			'100ms_50ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS,
			'400ms_50ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS,
			'off_40ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS,
			'off_100ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS,
			'off_400ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS,
			'off_10ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS,
			'100ms_100ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS,
			'100ms_400ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS,
			'50ms_50ms':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS,
			'off_off':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF,
			'400ms_off':_b.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF,
		}
		self.RPR0521_SYSTEM_CONTROL_INT_PIN={
			'no_init':_b.RPR0521_SYSTEM_CONTROL_INT_PIN_NO_INIT,
			'hi_z':_b.RPR0521_SYSTEM_CONTROL_INT_PIN_HI_Z,
		}
		self.RPR0521_INTERRUPT_INT_ASSERT={
			'reint':_b.RPR0521_INTERRUPT_INT_ASSERT_REINT,
			'stable':_b.RPR0521_INTERRUPT_INT_ASSERT_STABLE,
		}
		self.RPR0521_PS_CONTROL_PS_GAIN={
			'x2':_b.RPR0521_PS_CONTROL_PS_GAIN_X2,
			'x1':_b.RPR0521_PS_CONTROL_PS_GAIN_X1,
			'x4':_b.RPR0521_PS_CONTROL_PS_GAIN_X4,
		}
		self.RPR0521_INTERRUPT_INT_MODE={
			'ps_th_hysteresis':_b.RPR0521_INTERRUPT_INT_MODE_PS_TH_HYSTERESIS,
			'ps_th_outside_detection':_b.RPR0521_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION,
			'ps_th_h_active':_b.RPR0521_INTERRUPT_INT_MODE_PS_TH_H_ACTIVE,
			'forbidden':_b.RPR0521_INTERRUPT_INT_MODE_FORBIDDEN,
		}
		self.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG={
			'high':_b.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_HIGH,
			'too_high':_b.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_TOO_HIGH,
			'low':_b.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_LOW,
		}
		self.RPR0521_PS_CONTROL_PERSISTENCE={
			'consecutive_6':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6,
			'consecutive_7':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7,
			'consecutive_4':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4,
			'consecutive_5':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5,
			'consecutive_2':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2,
			'consecutive_3':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3,
			'consecutive_11':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11,
			'consecutive_10':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10,
			'drdy':_b.RPR0521_PS_CONTROL_PERSISTENCE_DRDY,
			'consecutive_12':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12,
			'consecutive_8':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8,
			'consecutive_9':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9,
			'consecutive_13':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13,
			'consecutive_14':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14,
			'consecutive_1':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1,
			'consecutive_15':_b.RPR0521_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15,
		}
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN={
			'x2':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2,
			'x1':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1,
			'x64':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64,
			'x128':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128,
		}
		self.RPR0521_INTERRUPT_INT_LATCH={
			'disabled':_b.RPR0521_INTERRUPT_INT_LATCH_DISABLED,
			'enabled':_b.RPR0521_INTERRUPT_INT_LATCH_ENABLED,
		}
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN={
			'x2':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2,
			'x1':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1,
			'x64':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64,
			'x128':_b.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128,
		}
		self.RPR0521_INTERRUPT_INT_TRIG={
			'by_both':_b.RPR0521_INTERRUPT_INT_TRIG_BY_BOTH,
			'inactive':_b.RPR0521_INTERRUPT_INT_TRIG_INACTIVE,
			'by_ps':_b.RPR0521_INTERRUPT_INT_TRIG_BY_PS,
			'by_als':_b.RPR0521_INTERRUPT_INT_TRIG_BY_ALS,
		}
		self.RPR0521_INTERRUPT_PS_INT_STATUS={
			'active':_b.RPR0521_INTERRUPT_PS_INT_STATUS_ACTIVE,
			'inactive':_b.RPR0521_INTERRUPT_PS_INT_STATUS_INACTIVE,
		}
		self.RPR0521_MODE_CONTROL_PS_OPERATING_MODE={
			'double_measurement':_b.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT,
			'normal':_b.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_NORMAL,
		}
		self.RPR0521_MODE_CONTROL_PS_PULSE={
			'330us':_b.RPR0521_MODE_CONTROL_PS_PULSE_330US,
			'200us':_b.RPR0521_MODE_CONTROL_PS_PULSE_200US,
		}
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT={
			'25ma':_b.RPR0521_ALS_PS_CONTROL_LED_CURRENT_25MA,
			'50ma':_b.RPR0521_ALS_PS_CONTROL_LED_CURRENT_50MA,
			'100ma':_b.RPR0521_ALS_PS_CONTROL_LED_CURRENT_100MA,
			'200ma':_b.RPR0521_ALS_PS_CONTROL_LED_CURRENT_200MA,
		}
		self.RPR0521_MODE_CONTROL_ALS_EN={
			'false':_b.RPR0521_MODE_CONTROL_ALS_EN_FALSE,
			'true':_b.RPR0521_MODE_CONTROL_ALS_EN_TRUE,
		}
		self.RPR0521_SYSTEM_CONTROL_SW_RESET={
			'start':_b.RPR0521_SYSTEM_CONTROL_SW_RESET_START,
			'not_started':_b.RPR0521_SYSTEM_CONTROL_SW_RESET_NOT_STARTED,
		}
		self.RPR0521_MODE_CONTROL_PS_EN={
			'false':_b.RPR0521_MODE_CONTROL_PS_EN_FALSE,
			'true':_b.RPR0521_MODE_CONTROL_PS_EN_TRUE,
		}
class masks(register_base):
	def __init__(self):
		self.RPR0521_SYSTEM_CONTROL_SW_RESET_MASK                 = 0x80         
		self.RPR0521_SYSTEM_CONTROL_INT_PIN_MASK                  = 0x40         
		self.RPR0521_SYSTEM_CONTROL_PART_MASK                     = 0x3F         
		self.RPR0521_MODE_CONTROL_ALS_EN_MASK                     = 0x80         
		self.RPR0521_MODE_CONTROL_PS_EN_MASK                      = 0x40         
		self.RPR0521_MODE_CONTROL_PS_PULSE_MASK                   = 0x20         
		self.RPR0521_MODE_CONTROL_PS_OPERATING_MODE_MASK          = 0x10         
		self.RPR0521_MODE_CONTROL_MEASUREMENT_TIME_MASK           = 0x0F         # (ALS)ms_(PS)ms
		self.RPR0521_ALS_PS_CONTROL_RESERVED67_MASK               = 0xC0         
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK           = 0x30         
		self.RPR0521_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK           = 0x0C         
		self.RPR0521_ALS_PS_CONTROL_LED_CURRENT_MASK              = 0x03         
		self.RPR0521_PS_CONTROL_AMBIENT_IR_FLAG_MASK              = 0xC0         
		self.RPR0521_PS_CONTROL_PS_GAIN_MASK                      = 0x30         
		self.RPR0521_PS_CONTROL_PERSISTENCE_MASK                  = 0x0F         
		self.RPR0521_INTERRUPT_PS_INT_STATUS_MASK                 = 0x80         
		self.RPR0521_INTERRUPT_ALS_INT_STATUS_MASK                = 0x40         
		self.RPR0521_INTERRUPT_INT_MODE_MASK                      = 0x30         
		self.RPR0521_INTERRUPT_INT_ASSERT_MASK                    = 0x08         
		self.RPR0521_INTERRUPT_INT_LATCH_MASK                     = 0x04         
		self.RPR0521_INTERRUPT_INT_TRIG_MASK                      = 0x03         
		self.RPR0521_MANUFACT_ID_MASK                             = 0xFF         