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
		self.BH1730_CONTROL                                       = 0x80         
		self.BH1730_TIMING                                        = 0x81         # ITIME. Integration time is (256-ITIME)*2,7ms (0 means manual integration)
		self.BH1730_INTERRUPT                                     = 0x82         
		self.BH1730_THLLOW                                        = 0x83         
		self.BH1730_THLHIGH                                       = 0x84         
		self.BH1730_THHLOW                                        = 0x85         
		self.BH1730_THHHIGH                                       = 0x86         
		self.BH1730_GAIN                                          = 0x87         
		self.BH1730_OPART_ID                                      = 0x92         
		self.BH1730_DATA0LOW                                      = 0x94         
		self.BH1730_DATA0HIGH                                     = 0x95         
		self.BH1730_DATA1LOW                                      = 0x96         
		self.BH1730_DATA1HIGH                                     = 0x97         
		self.BH1730_INT_RESET                                     = 0xE1         # Reset interrupt
		self.BH1730_RESET                                         = 0xE4         # Software reset
class bits(register_base):
	def __init__(self):
		self.BH1730_CONTROL_ADC_INTR_INACTIVE                     = (0x00 << 5)  
		self.BH1730_CONTROL_ADC_INTR_ACTIVE                       = (0x01 << 5)  
		self.BH1730_CONTROL_ADC_INTR                              = (0x01 << 5)  
		self.BH1730_CONTROL_ADC_VALID                             = (0x01 << 4)  
		self.BH1730_CONTROL_ONE_TIME_CONTINOUS                    = (0x00 << 3)  
		self.BH1730_CONTROL_ONE_TIME_ONETIME                      = (0x01 << 3)  
		self.BH1730_CONTROL_ONE_TIME                              = (0x01 << 3)  
		self.BH1730_CONTROL_DATA_SEL_TYPE0_AND_1                  = (0x00 << 2)  
		self.BH1730_CONTROL_DATA_SEL_TYPE0                        = (0x01 << 2)  
		self.BH1730_CONTROL_DATA_SEL                              = (0x01 << 2)  
		self.BH1730_CONTROL_ADC_EN_DISABLE                        = (0x00 << 1)  
		self.BH1730_CONTROL_ADC_EN_ENABLE                         = (0x01 << 1)  
		self.BH1730_CONTROL_ADC_EN                                = (0x01 << 1)  
		self.BH1730_CONTROL_POWER_DISABLE                         = (0x00 << 0)  
		self.BH1730_CONTROL_POWER_ENABLE                          = (0x01 << 0)  
		self.BH1730_CONTROL_POWER                                 = (0x01 << 0)  
		self.BH1730_INTERRUPT_RES7                                = (0x01 << 7)  # reset by writing 0
		self.BH1730_INTERRUPT_INT_STOP_CONTINUOUS                 = (0x00 << 6)  
		self.BH1730_INTERRUPT_INT_STOP_STOPPED                    = (0x01 << 6)  
		self.BH1730_INTERRUPT_INT_STOP                            = (0x01 << 6)  
		self.BH1730_INTERRUPT_RES5                                = (0x01 << 5)  # reset by writing 0
		self.BH1730_INTERRUPT_INT_EN_INVALID                      = (0x00 << 4)  
		self.BH1730_INTERRUPT_INT_EN_VALID                        = (0x01 << 4)  
		self.BH1730_INTERRUPT_INT_EN                              = (0x01 << 4)  
		self.BH1730_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT    = (0x00 << 0)  
		self.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT    = (0x01 << 0)  
		self.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME         = (0x02 << 0)  
		self.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME         = (0x03 << 0)  
		self.BH1730_GAIN_RES_WRITE00000                           = (0x00 << 3)  
		self.BH1730_GAIN_GAIN_X1_GAIN                             = (0x00 << 0)  
		self.BH1730_GAIN_GAIN_X2_GAIN                             = (0x01 << 0)  
		self.BH1730_GAIN_GAIN_X64_GAIN                            = (0x02 << 0)  
		self.BH1730_GAIN_GAIN_X128_GAIN                           = (0x03 << 0)  
		self.BH1730_OPART_ID_WIA_ID                               = (0x71 << 0)  # WHO_AM_I -value
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1730_CONTROL_ADC_INTR={
			'ACTIVE':_b.BH1730_CONTROL_ADC_INTR_ACTIVE,
			'INACTIVE':_b.BH1730_CONTROL_ADC_INTR_INACTIVE,
		}
		self.BH1730_INTERRUPT_PERSIST={
			'UPDATE_AFTER_3_SAME':_b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME,
			'UPDATE_AFTER_MEASUREMENT':_b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,
			'UPDATE_AFTER_2_SAME':_b.BH1730_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,
			'TOGGLE_AFTER_MEASUREMENT':_b.BH1730_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,
		}
		self.BH1730_INTERRUPT_INT_EN={
			'VALID':_b.BH1730_INTERRUPT_INT_EN_VALID,
			'INVALID':_b.BH1730_INTERRUPT_INT_EN_INVALID,
		}
		self.BH1730_CONTROL_ONE_TIME={
			'ONETIME':_b.BH1730_CONTROL_ONE_TIME_ONETIME,
			'CONTINOUS':_b.BH1730_CONTROL_ONE_TIME_CONTINOUS,
		}
		self.BH1730_GAIN_GAIN={
			'X64_GAIN':_b.BH1730_GAIN_GAIN_X64_GAIN,
			'X1_GAIN':_b.BH1730_GAIN_GAIN_X1_GAIN,
			'X2_GAIN':_b.BH1730_GAIN_GAIN_X2_GAIN,
			'X128_GAIN':_b.BH1730_GAIN_GAIN_X128_GAIN,
		}
		self.BH1730_INTERRUPT_INT_STOP={
			'CONTINUOUS':_b.BH1730_INTERRUPT_INT_STOP_CONTINUOUS,
			'STOPPED':_b.BH1730_INTERRUPT_INT_STOP_STOPPED,
		}
		self.BH1730_CONTROL_ADC_EN={
			'DISABLE':_b.BH1730_CONTROL_ADC_EN_DISABLE,
			'ENABLE':_b.BH1730_CONTROL_ADC_EN_ENABLE,
		}
		self.BH1730_CONTROL_DATA_SEL={
			'TYPE0_AND_1':_b.BH1730_CONTROL_DATA_SEL_TYPE0_AND_1,
			'TYPE0':_b.BH1730_CONTROL_DATA_SEL_TYPE0,
		}
		self.BH1730_CONTROL_POWER={
			'DISABLE':_b.BH1730_CONTROL_POWER_DISABLE,
			'ENABLE':_b.BH1730_CONTROL_POWER_ENABLE,
		}
class masks(register_base):
	def __init__(self):
		self.BH1730_CONTROL_ADC_INTR_MASK                         = 0x20         
		self.BH1730_CONTROL_ONE_TIME_MASK                         = 0x08         
		self.BH1730_CONTROL_DATA_SEL_MASK                         = 0x04         
		self.BH1730_CONTROL_ADC_EN_MASK                           = 0x02         
		self.BH1730_CONTROL_POWER_MASK                            = 0x01         
		self.BH1730_INTERRUPT_INT_STOP_MASK                       = 0x40         
		self.BH1730_INTERRUPT_INT_EN_MASK                         = 0x10         
		self.BH1730_INTERRUPT_PERSIST_MASK                        = 0x0F         # Threshold persistent. Samples to cross threshold before interrupt updated. Zero means interrupt active at each measurement end.
		self.BH1730_GAIN_RES_MASK                                 = 0xF8         
		self.BH1730_GAIN_GAIN_MASK                                = 0x07         
		self.BH1730_OPART_ID_WIA_MASK                             = 0xFF         