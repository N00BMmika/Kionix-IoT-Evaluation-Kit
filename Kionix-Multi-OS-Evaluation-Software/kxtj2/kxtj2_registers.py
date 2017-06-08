# The MIT License (MIT)
# Copyright (c) 2017 Kionix Inc.
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
		self.KXTJ2_OUTX_L                                         = 0x06         # output register x
		self.KXTJ2_OUTX_H                                         = 0x07         
		self.KXTJ2_OUTY_L                                         = 0x08         # output register y
		self.KXTJ2_OUTY_H                                         = 0x09         
		self.KXTJ2_OUTZ_L                                         = 0x0A         # output register z
		self.KXTJ2_OUTZ_H                                         = 0x0B         
		self.KXTJ2_DCST_RESP                                      = 0x0C         # This register can be used to verify proper integrated circuit functionality
		self.KXTJ2_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition, as it can be factory written to a known byte value.
		self.KXTJ2_INT_SOURCE1                                    = 0x16         # This register reports which function caused an interrupt.
		self.KXTJ2_INT_SOURCE2                                    = 0x17         # This register reports the axis and direction of detected motion
		self.KXTJ2_STATUS_REG                                     = 0x18         # This register reports the status of the interrupt
		self.KXTJ2_INT_REL                                        = 0x1A         
		self.KXTJ2_CTRL_REG1                                      = 0x1B         # Read/write control register that controls the main feature set
		self.KXTJ2_CTRL_REG2                                      = 0x1D         # Read/write control register that provides more feature set control
		self.KXTJ2_INT_CTRL_REG1                                  = 0x1E         # This register controls the settings for the physical interrupt pin
		self.KXTJ2_INT_CTRL_REG2                                  = 0x1F         # This register controls which axis and direction of detected motion can cause an interrupt
		self.KXTJ2_DATA_CTRL_REG                                  = 0x21         # Read/write control register that configures the acceleration outputs
		self.KXTJ2_WAKEUP_TIMER                                   = 0x29         
		self.KXTJ2_SELF_TEST                                      = 0x3A         # When 0xCA is written to this register, the MEMS self-test function is enabled
		self.KXTJ2_WAKEUP_THRESHOLD                               = 0x6A         
class bits(register_base):
	def __init__(self):
		self.KXTJ2_DCST_RESP_COM_TEST_BEFORE                      = (0x55 << 0)  # before set
		self.KXTJ2_DCST_RESP_COM_TEST_AFTER                       = (0xAA << 0)  # after set
		self.KXTJ2_WHO_AM_I_WIA_ID                                = (0x09 << 0)  # WHO_AM_I -value
		self.KXTJ2_INT_SOURCE1_DRDY                               = (0x01 << 4)  # indicates that new acceleration data
		self.KXTJ2_INT_SOURCE1_WUFS                               = (0x01 << 1)  # Wake up
		self.KXTJ2_INT_SOURCE2_XNWU                               = (0x01 << 5)  # x-
		self.KXTJ2_INT_SOURCE2_XPWU                               = (0x01 << 4)  # x+
		self.KXTJ2_INT_SOURCE2_YNWU                               = (0x01 << 3)  # y-
		self.KXTJ2_INT_SOURCE2_YPWU                               = (0x01 << 2)  # y+
		self.KXTJ2_INT_SOURCE2_ZNWU                               = (0x01 << 1)  # z-
		self.KXTJ2_INT_SOURCE2_ZPWU                               = (0x01 << 0)  # z+
		self.KXTJ2_STATUS_REG_INT                                 = (0x01 << 4)  # reports the combined (OR) interrupt information of DRDY and WUFS in the interrupt source register
		self.KXTJ2_CTRL_REG1_PC                                   = (0x01 << 7)  # controls the operating mode of the KXTJ2
		self.KXTJ2_CTRL_REG1_RES                                  = (0x01 << 6)  # determines the performance mode of the KXTJ2
		self.KXTJ2_CTRL_REG1_DRDYE                                = (0x01 << 5)  # enables the reporting of the availability of new acceleration data as an interrupt
		self.KXTJ2_CTRL_REG1_GSEL_2G                              = (0x00 << 3)  # 2g range
		self.KXTJ2_CTRL_REG1_GSEL_4G                              = (0x01 << 3)  # 4g range
		self.KXTJ2_CTRL_REG1_GSEL_8G                              = (0x02 << 3)  # 8g range
		self.KXTJ2_CTRL_REG1_GSEL_8G_14B                          = (0x03 << 3)  # 8g range with 14b resolution
		self.KXTJ2_CTRL_REG1_WUFE                                 = (0x01 << 1)  # enables the Wake Up (motion detect) function.
		self.KXTJ2_CTRL_REG2_SRST                                 = (0x01 << 7)  # initiates software reset
		self.KXTJ2_CTRL_REG2_DCST                                 = (0x01 << 4)  # initiates the digital communication self-test function.
		self.KXTJ2_CTRL_REG2_OWUF_0P781                           = (0x00 << 0)  # 0.78Hz
		self.KXTJ2_CTRL_REG2_OWUF_1P563                           = (0x01 << 0)  # 1.563Hz
		self.KXTJ2_CTRL_REG2_OWUF_3P125                           = (0x02 << 0)  # 3.125Hz
		self.KXTJ2_CTRL_REG2_OWUF_6P25                            = (0x03 << 0)  # 6.25Hz
		self.KXTJ2_CTRL_REG2_OWUF_12P5                            = (0x04 << 0)  # 12.5Hz
		self.KXTJ2_CTRL_REG2_OWUF_25                              = (0x05 << 0)  # 25Hz
		self.KXTJ2_CTRL_REG2_OWUF_50                              = (0x06 << 0)  # 50Hz
		self.KXTJ2_CTRL_REG2_OWUF_100                             = (0x07 << 0)  # 100Hz
		self.KXTJ2_INT_CTRL_REG1_IEN                              = (0x01 << 5)  # enables/disables the physical interrupt pin
		self.KXTJ2_INT_CTRL_REG1_IEA                              = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KXTJ2_INT_CTRL_REG1_IEL                              = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KXTJ2_INT_CTRL_REG1_STPOL                            = (0x01 << 1)  # selftest polarity
		self.KXTJ2_INT_CTRL_REG2_XNWU                             = (0x01 << 5)  # x-
		self.KXTJ2_INT_CTRL_REG2_XPWU                             = (0x01 << 4)  # x+
		self.KXTJ2_INT_CTRL_REG2_YNWU                             = (0x01 << 3)  # y-
		self.KXTJ2_INT_CTRL_REG2_YPWU                             = (0x01 << 2)  # y+
		self.KXTJ2_INT_CTRL_REG2_ZNWU                             = (0x01 << 1)  # z-
		self.KXTJ2_INT_CTRL_REG2_ZPWU                             = (0x01 << 0)  # z+
		self.KXTJ2_DATA_CTRL_REG_OSA_12P5                         = (0x00 << 0)  # 12.5Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_25                           = (0x01 << 0)  # 25Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_50                           = (0x02 << 0)  # 50Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_100                          = (0x03 << 0)  # 100Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_200                          = (0x04 << 0)  # 200Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_400                          = (0x05 << 0)  # 400Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_800                          = (0x06 << 0)  # 800Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_1600                         = (0x07 << 0)  # 1600Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_0P781                        = (0x08 << 0)  # 0.78Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_1P563                        = (0x09 << 0)  # 1.563Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_3P125                        = (0x0A << 0)  # 3.125Hz
		self.KXTJ2_DATA_CTRL_REG_OSA_6P25                         = (0x0B << 0)  # 6.25Hz
		self.KXTJ2_SELF_TEST_TEST_ENABLE                          = (0xCA << 0)  # charge on
		self.KXTJ2_SELF_TEST_TEST_DISABLE                         = (0x00 << 0)  # charge off
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KXTJ2_SELF_TEST_TEST={
			'ENABLE':_b.KXTJ2_SELF_TEST_TEST_ENABLE,
			'DISABLE':_b.KXTJ2_SELF_TEST_TEST_DISABLE,
		}
		self.KXTJ2_DATA_CTRL_REG_OSA={
			'25':_b.KXTJ2_DATA_CTRL_REG_OSA_25,
			'0p781':_b.KXTJ2_DATA_CTRL_REG_OSA_0P781,
			'200':_b.KXTJ2_DATA_CTRL_REG_OSA_200,
			'12p5':_b.KXTJ2_DATA_CTRL_REG_OSA_12P5,
			'1600':_b.KXTJ2_DATA_CTRL_REG_OSA_1600,
			'50':_b.KXTJ2_DATA_CTRL_REG_OSA_50,
			'1p563':_b.KXTJ2_DATA_CTRL_REG_OSA_1P563,
			'3p125':_b.KXTJ2_DATA_CTRL_REG_OSA_3P125,
			'400':_b.KXTJ2_DATA_CTRL_REG_OSA_400,
			'100':_b.KXTJ2_DATA_CTRL_REG_OSA_100,
			'800':_b.KXTJ2_DATA_CTRL_REG_OSA_800,
			'6p25':_b.KXTJ2_DATA_CTRL_REG_OSA_6P25,
		}
		self.KXTJ2_CTRL_REG1_GSEL={
			'4G':_b.KXTJ2_CTRL_REG1_GSEL_4G,
			'2G':_b.KXTJ2_CTRL_REG1_GSEL_2G,
			'8G':_b.KXTJ2_CTRL_REG1_GSEL_8G,
			'8G_14b':_b.KXTJ2_CTRL_REG1_GSEL_8G_14B,
		}
		self.KXTJ2_CTRL_REG2_OWUF={
			'25':_b.KXTJ2_CTRL_REG2_OWUF_25,
			'0p781':_b.KXTJ2_CTRL_REG2_OWUF_0P781,
			'12p5':_b.KXTJ2_CTRL_REG2_OWUF_12P5,
			'50':_b.KXTJ2_CTRL_REG2_OWUF_50,
			'1p563':_b.KXTJ2_CTRL_REG2_OWUF_1P563,
			'3p125':_b.KXTJ2_CTRL_REG2_OWUF_3P125,
			'100':_b.KXTJ2_CTRL_REG2_OWUF_100,
			'6p25':_b.KXTJ2_CTRL_REG2_OWUF_6P25,
		}
		self.KXTJ2_DCST_RESP_COM_TEST={
			'AFTER':_b.KXTJ2_DCST_RESP_COM_TEST_AFTER,
			'BEFORE':_b.KXTJ2_DCST_RESP_COM_TEST_BEFORE,
		}
class masks(register_base):
	def __init__(self):
		self.KXTJ2_DCST_RESP_COM_TEST_MASK                        = 0xFF         
		self.KXTJ2_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KXTJ2_CTRL_REG1_GSEL_MASK                            = 0x18         # selects the acceleration range of the accelerometer outputs
		self.KXTJ2_CTRL_REG2_OWUF_MASK                            = 0x07         # sets the Output Data Rate for the Wake Up function
		self.KXTJ2_DATA_CTRL_REG_OSA_MASK                         = 0x0F         # sets the output data rate (ODR)
		self.KXTJ2_SELF_TEST_TEST_MASK                            = 0xFF         