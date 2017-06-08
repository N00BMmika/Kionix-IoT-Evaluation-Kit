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
		self.BH1726_REGISTER_DUMP_START                           = 0x80         
		self.BH1726_CONTROL                                       = 0x80         
		self.BH1726_TIMING                                        = 0x81         
		self.BH1726_INTERRUPT                                     = 0x82         
		self.BH1726_THLLOW                                        = 0x83         
		self.BH1726_THLHIGH                                       = 0x84         
		self.BH1726_THHLOW                                        = 0x85         
		self.BH1726_THHHIGH                                       = 0x86         
		self.BH1726_GAIN                                          = 0x87         
		self.BH1726_OPART_ID                                      = 0x92         
		self.BH1726_DATA0LOW                                      = 0x94         
		self.BH1726_DATA0HIGH                                     = 0x95         
		self.BH1726_DATA1LOW                                      = 0x96         
		self.BH1726_DATA1HIGH                                     = 0x97         
		self.BH1726_WAIT                                          = 0x98         
		self.BH1726_INT_RESET                                     = 0xE1         # Reset interrupt
		self.BH1726_RESET                                         = 0xE4         # Software reset
		self.BH1726_REGISTER_DUMP_END                             = 0x98         
class bits(register_base):
	def __init__(self):
		self.BH1726_CONTROL_ADC_INTR_INACTIVE                     = (0x00 << 5)  
		self.BH1726_CONTROL_ADC_INTR_ACTIVE                       = (0x01 << 5)  
		self.BH1726_CONTROL_ADC_VALID                             = (0x01 << 4)  
		self.BH1726_CONTROL_ADC_EN_DISABLE                        = (0x00 << 1)  
		self.BH1726_CONTROL_ADC_EN_ENABLE                         = (0x01 << 1)  
		self.BH1726_CONTROL_POWER_DISABLE                         = (0x00 << 0)  
		self.BH1726_CONTROL_POWER_ENABLE                          = (0x01 << 0)  
		self.BH1726_INTERRUPT_RES7                                = (0x01 << 7)  # reset by writing 0
		self.BH1726_INTERRUPT_INT_LATCH_YES                       = (0x00 << 5)  
		self.BH1726_INTERRUPT_INT_LATCH_NO                        = (0x01 << 5)  
		self.BH1726_INTERRUPT_INT_EN_INVALID                      = (0x00 << 4)  
		self.BH1726_INTERRUPT_INT_EN_VALID                        = (0x01 << 4)  
		self.BH1726_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT    = (0x00 << 0)  
		self.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT    = (0x01 << 0)  
		self.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME         = (0x02 << 0)  
		self.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME         = (0x03 << 0)  
		self.BH1726_GAIN_GAIN0_X1                                 = (0x00 << 2)  
		self.BH1726_GAIN_GAIN0_X2                                 = (0x01 << 2)  
		self.BH1726_GAIN_GAIN0_X64                                = (0x02 << 2)  
		self.BH1726_GAIN_GAIN0_X128                               = (0x03 << 2)  
		self.BH1726_GAIN_GAIN1_X1                                 = (0x00 << 0)  
		self.BH1726_GAIN_GAIN1_X2                                 = (0x01 << 0)  
		self.BH1726_GAIN_GAIN1_X64                                = (0x02 << 0)  
		self.BH1726_GAIN_GAIN1_X128                               = (0x03 << 0)  
		self.BH1726_OPART_ID_WIA_ID                               = (0x72 << 0)  # WHO_AM_I -value
		self.BH1726_WAIT_WAIT_NO                                  = (0x00 << 0)  
		self.BH1726_WAIT_WAIT_300MS                               = (0x01 << 0)  # after each measurement (low current consumption mode)
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1726_INTERRUPT_INT_LATCH={
			'yes':_b.BH1726_INTERRUPT_INT_LATCH_YES,
			'no':_b.BH1726_INTERRUPT_INT_LATCH_NO,
		}
		self.BH1726_CONTROL_ADC_EN={
			'Disable':_b.BH1726_CONTROL_ADC_EN_DISABLE,
			'Enable':_b.BH1726_CONTROL_ADC_EN_ENABLE,
		}
		self.BH1726_GAIN_GAIN0={
			'x2':_b.BH1726_GAIN_GAIN0_X2,
			'x1':_b.BH1726_GAIN_GAIN0_X1,
			'x64':_b.BH1726_GAIN_GAIN0_X64,
			'x128':_b.BH1726_GAIN_GAIN0_X128,
		}
		self.BH1726_INTERRUPT_INT_EN={
			'valid':_b.BH1726_INTERRUPT_INT_EN_VALID,
			'invalid':_b.BH1726_INTERRUPT_INT_EN_INVALID,
		}
		self.BH1726_GAIN_GAIN1={
			'x2':_b.BH1726_GAIN_GAIN1_X2,
			'x1':_b.BH1726_GAIN_GAIN1_X1,
			'x64':_b.BH1726_GAIN_GAIN1_X64,
			'x128':_b.BH1726_GAIN_GAIN1_X128,
		}
		self.BH1726_CONTROL_ADC_INTR={
			'active':_b.BH1726_CONTROL_ADC_INTR_ACTIVE,
			'inactive':_b.BH1726_CONTROL_ADC_INTR_INACTIVE,
		}
		self.BH1726_CONTROL_POWER={
			'Disable':_b.BH1726_CONTROL_POWER_DISABLE,
			'Enable':_b.BH1726_CONTROL_POWER_ENABLE,
		}
		self.BH1726_WAIT_WAIT={
			'300ms':_b.BH1726_WAIT_WAIT_300MS,
			'no':_b.BH1726_WAIT_WAIT_NO,
		}
		self.BH1726_INTERRUPT_PERSIST={
			'update_after_3_same':_b.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME,
			'update_after_measurement':_b.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,
			'update_after_2_same':_b.BH1726_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,
			'toggle_after_measurement':_b.BH1726_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,
		}
class masks(register_base):
	def __init__(self):
		self.BH1726_CONTROL_ADC_INTR_MASK                         = 0x20         
		self.BH1726_CONTROL_ADC_EN_MASK                           = 0x02         
		self.BH1726_CONTROL_POWER_MASK                            = 0x01         
		self.BH1726_INTERRUPT_INT_LATCH_MASK                      = 0x20         
		self.BH1726_INTERRUPT_INT_EN_MASK                         = 0x10         
		self.BH1726_INTERRUPT_PERSIST_MASK                        = 0x0F         # Threshold persistent. Samples to cross threshold before interrupt updated. Zero means interrupt active at each measurement end.
		self.BH1726_GAIN_GAIN0_MASK                               = 0x0C         # Gain of data0 resolution
		self.BH1726_GAIN_GAIN1_MASK                               = 0x03         # Gain of data1 resolution
		self.BH1726_OPART_ID_WIA_MASK                             = 0xFF         
		self.BH1726_WAIT_WAIT_MASK                                = 0x01         