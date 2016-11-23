# The MIT License (MIT)
# Copyright (c) 2016 Rohm Semiconductor
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
		self.BM1383GLV_PRESSURE_MIN                               = 0x12C        # [hPa]
		self.BM1383GLV_PRESSURE_MAX                               = 0x44C        # [hPa]
		self.BM1383GLV_REGISTER_DUMP_START                        = 0x10         
		self.BM1383GLV_ID_REG                                     = 0x10         
		self.BM1383GLV_RESET_CONTROL_REG                          = 0x11         # All control registers are accessible only when POWER is UP and SLEEP is OFF.
		self.BM1383GLV_POWER_REG                                  = 0x12         
		self.BM1383GLV_SLEEP_REG                                  = 0x13         
		self.BM1383GLV_MODE_CONTROL_REG                           = 0x14         
		self.BM1383GLV_INT_HIGH_TRESHOLD_MSB                      = 0x15         # MSB of the high threshold value for pressure interrupt generation.
		self.BM1383GLV_INT_HIGH_TRESHOLD_LSB                      = 0x16         # LSB of the high threshold value for pressure interrupt generation.
		self.BM1383GLV_INT_LOW_TRESHOLD_MSB                       = 0x17         
		self.BM1383GLV_INT_LOW_TRESHOLD_LSB                       = 0x18         
		self.BM1383GLV_INT_CONTROL_REG                            = 0x19         
		self.BM1383GLV_TEMPERATURE_OUT_MSB                        = 0x1A         # TEMP_OUT: [15] sign ; [14:5] integer ; [4:0] decimal (2's complement numbers)
		self.BM1383GLV_TEMPERATURE_OUT_LSB                        = 0x1B         # Temperature value [C]= TEMP_OUT[15:0]/32
		self.BM1383GLV_PRESSURE_OUT_MSB                           = 0x1C         # PRESS_OUT[15:5] integer part of pressure value
		self.BM1383GLV_PRESSURE_OUT_LSB                           = 0x1D         # PRESS_OUT[4:0] PRESS_OUT_XL[5:0] decimal part of pressure value
		self.BM1383GLV_PRESSURE_OUT_DECIMAL                       = 0x1E         # Pressurevalue[hPa] = { PRESS_OUT[15:8] PRESS_OUT[7:0] PRESS_OUT_XL[5:0] } / 2048
		self.BM1383GLV_REGISTER_DUMP_END                          = 0x1E         
class bits(register_base):
	def __init__(self):
		self.BM1383GLV_ID_REG_MANUFACTURER_ID                     = (0x03 << 4)  
		self.BM1383GLV_ID_REG_PART_ID                             = (0x01 << 0)  
		self.BM1383GLV_RESET_CONTROL_REG_SW_RESET_NONE            = (0x00 << 7)  
		self.BM1383GLV_RESET_CONTROL_REG_SW_RESET_EXECUTE         = (0x01 << 7)  
		self.BM1383GLV_RESET_CONTROL_REG_INT_RESET_ACTIVE         = (0x00 << 6)  
		self.BM1383GLV_RESET_CONTROL_REG_INT_RESET_INACTIVE       = (0x01 << 6)  # int terminal high impedance on inactive state
		self.BM1383GLV_RESET_CONTROL_REG_RESERVED_WRITE0          = (0x00 << 0)  # write 000000
		self.BM1383GLV_POWER_REG_RESERVED_WRITE0                  = (0x00 << 1)  
		self.BM1383GLV_POWER_REG_POWER_DOWN                       = (0x00 << 0)  
		self.BM1383GLV_POWER_REG_POWER_UP                         = (0x01 << 0)  
		self.BM1383GLV_SLEEP_REG_RESERVED_WRITE0                  = (0x00 << 1)  
		self.BM1383GLV_SLEEP_REG_SLEEP_ON                         = (0x00 << 0)  
		self.BM1383GLV_SLEEP_REG_SLEEP_OFF                        = (0x01 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_SINGLE            = (0x00 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_2_TIMES           = (0x01 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_4_TIMES           = (0x02 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_8_TIMES           = (0x03 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_16_TIMES          = (0x04 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_32_TIMES          = (0x05 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_64_TIMES          = (0x06 << 5)  
		self.BM1383GLV_MODE_CONTROL_REG_RESERVED_WRITE0           = (0x00 << 3)  # write 00
		self.BM1383GLV_MODE_CONTROL_REG_MODE_STANDBY              = (0x00 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_ONE_SHOT             = (0x01 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_50MS                 = (0x02 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_100MS                = (0x03 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_200MS                = (0x04 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_PROHIBITED5          = (0x05 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_PROHIBITED6          = (0x06 << 0)  
		self.BM1383GLV_MODE_CONTROL_REG_MODE_PROHIBITED7          = (0x07 << 0)  
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_HIGH_IN_LIMITS    = (0x00 << 7)  
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_HIGH_CROSSED      = (0x01 << 7)  
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_LOW_IN_LIMITS     = (0x00 << 6)  
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_LOW_CROSSED       = (0x01 << 6)  
		self.BM1383GLV_INT_CONTROL_REG_INT_HIGH_DISABLE           = (0x00 << 5)  
		self.BM1383GLV_INT_CONTROL_REG_INT_HIGH_ENABLE            = (0x01 << 5)  
		self.BM1383GLV_INT_CONTROL_REG_INT_LOW_DISABLE            = (0x00 << 4)  
		self.BM1383GLV_INT_CONTROL_REG_INT_LOW_ENABLE             = (0x01 << 4)  
		self.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_ENABLE          = (0x00 << 3)  # pull up resistor in INT terminals
		self.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_DISABLE         = (0x01 << 3)  # no pull up resistor in INT terminals
		self.BM1383GLV_INT_CONTROL_REG_RESERVED_RES               = (0x00 << 2)  
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_KEEP_UNTIL_CLEARED = (0x00 << 1)  # terminal is latched until interrupt is cleared
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_CONTINUOUS_UPDATE = (0x01 << 1)  # terminal is updated after each measurement
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_DISABLE          = (0x00 << 0)  
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_ENABLE           = (0x01 << 0)  
class masks(register_base):
	def __init__(self):
		self.BM1383GLV_ID_REG_MANUFACTURER_MASK                   = 0xF0         
		self.BM1383GLV_ID_REG_PART_MASK                           = 0x0F         
		self.BM1383GLV_RESET_CONTROL_REG_SW_RESET_MASK            = 0x80         
		self.BM1383GLV_RESET_CONTROL_REG_INT_RESET_MASK           = 0x40         
		self.BM1383GLV_RESET_CONTROL_REG_RESERVED_MASK            = 0x3F         
		self.BM1383GLV_POWER_REG_RESERVED_MASK                    = 0xFE         
		self.BM1383GLV_POWER_REG_POWER_MASK                       = 0x01         
		self.BM1383GLV_SLEEP_REG_RESERVED_MASK                    = 0xFE         
		self.BM1383GLV_SLEEP_REG_SLEEP_MASK                       = 0x01         
		self.BM1383GLV_MODE_CONTROL_REG_AVE_NUM_MASK              = 0xE0         
		self.BM1383GLV_MODE_CONTROL_REG_RESERVED_MASK             = 0x18         
		self.BM1383GLV_MODE_CONTROL_REG_MODE_MASK                 = 0x07         
		self.BM1383GLV_INT_HIGH_TRESHOLD_MSB_ALLBITS_MASK         = 0xFF         
		self.BM1383GLV_INT_HIGH_TRESHOLD_LSB_ALLBITS_MASK         = 0xFF         
		self.BM1383GLV_INT_LOW_TRESHOLD_MSB_ALLBITS_MASK          = 0xFF         
		self.BM1383GLV_INT_LOW_TRESHOLD_LSB_ALLBITS_MASK          = 0xFF         
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_HIGH_MASK         = 0x80         
		self.BM1383GLV_INT_CONTROL_REG_TRESHOLD_LOW_MASK          = 0x40         
		self.BM1383GLV_INT_CONTROL_REG_INT_HIGH_MASK              = 0x20         
		self.BM1383GLV_INT_CONTROL_REG_INT_LOW_MASK               = 0x10         
		self.BM1383GLV_INT_CONTROL_REG_INT_PULLUP_MASK            = 0x08         
		self.BM1383GLV_INT_CONTROL_REG_RESERVED_MASK              = 0x04         
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_STATE_MASK       = 0x02         
		self.BM1383GLV_INT_CONTROL_REG_INTERRUPT_MASK             = 0x01         
		self.BM1383GLV_TEMPERATURE_OUT_MSB_ALLBITS_MASK           = 0xFF         
		self.BM1383GLV_TEMPERATURE_OUT_LSB_ALLBITS_MASK           = 0xFF         
		self.BM1383GLV_PRESSURE_OUT_MSB_ALLBITS_MASK              = 0xFF         
		self.BM1383GLV_PRESSURE_OUT_LSB_ALLBITS_MASK              = 0xFF         
		self.BM1383GLV_PRESSURE_OUT_DECIMAL_ALLBITS_MASK          = 0x3F         