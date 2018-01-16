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
		self.KXCNL_INFO1                                          = 0x0D         # This register can be used for optional supplier information.
		self.KXCNL_INFO2                                          = 0x0E         # A second register can be used for optional supplier information.
		self.KXCNL_WIA                                            = 0x0F         # This register can be used for supplier recognition (Who I Am ID),
		self.KXCNL_OUTX_L                                         = 0x10         
		self.KXCNL_OUTX_H                                         = 0x11         
		self.KXCNL_OUTY_L                                         = 0x12         
		self.KXCNL_OUTY_H                                         = 0x13         
		self.KXCNL_OUTZ_L                                         = 0x14         
		self.KXCNL_OUTZ_H                                         = 0x15         
		self.KXCNL_LC_L                                           = 0x16         # These two registers contain up to 16-bits of long counter information.
		self.KXCNL_LC_H                                           = 0x17         
		self.KXCNL_STAT                                           = 0x18         # This register reports the status of the accelerometer outputs
		self.KXCNL_PEAK1                                          = 0x19         # Peak detector value for Next condition of State Program 1.
		self.KXCNL_PEAK2                                          = 0x1A         # Peak detector value for Next condition of State Program 2
		self.KXCNL_CNTL1                                          = 0x1B         # Read/write control register that controls the main feature set
		self.KXCNL_CNTL2                                          = 0x1C         # Read/write control register that controls the State Program 1.
		self.KXCNL_CNTL3                                          = 0x1D         # Read/write control register that controls the State Program 2.
		self.KXCNL_CNTL4                                          = 0x1E         # Read/write control register that controls several functions of the KXCNL.
		self.KXCNL_THRS3                                          = 0x1F         
		self.KXCNL_OFF_X                                          = 0x20         
		self.KXCNL_OFF_Y                                          = 0x21         
		self.KXCNL_OFF_Z                                          = 0x22         
		self.KXCNL_CS_X                                           = 0x24         
		self.KXCNL_CS_Y                                           = 0x25         
		self.KXCNL_CS_Z                                           = 0x26         
		self.KXCNL_X_DEBUG                                        = 0x28         
		self.KXCNL_Y_DEBUG                                        = 0x29         
		self.KXCNL_Z_DEBUG                                        = 0x2A         
		self.KXCNL_VFC_1                                          = 0x2C         
		self.KXCNL_VFC_2                                          = 0x2D         
		self.KXCNL_VFC_3                                          = 0x2E         
		self.KXCNL_VFC_4                                          = 0x2F         
		self.KXCNL_ST1_1                                          = 0x40         
		self.KXCNL_TIM4_1                                         = 0x50         
		self.KXCNL_TIM3_1                                         = 0x51         
		self.KXCNL_TIM2_1_L                                       = 0x52         
		self.KXCNL_TIM2_1_H                                       = 0x53         
		self.KXCNL_TIM1_1_L                                       = 0x54         
		self.KXCNL_TIM1_1_H                                       = 0x55         
		self.KXCNL_THRS2_1                                        = 0x56         
		self.KXCNL_THRS1_1                                        = 0x57         
		self.KXCNL_SA1                                            = 0x59         
		self.KXCNL_MA1                                            = 0x5A         
		self.KXCNL_SETT1                                          = 0x5B         
		self.KXCNL_PPRP1                                          = 0x5C         
		self.KXCNL_TC1_L                                          = 0x5D         
		self.KXCNL_TC1_H                                          = 0x5E         
		self.KXCNL_OUTS1                                          = 0x5F         
		self.KXCNL_ST1_2                                          = 0x60         
		self.KXCNL_TIM4_2                                         = 0x70         
		self.KXCNL_TIM3_2                                         = 0x71         
		self.KXCNL_TIM2_2_L                                       = 0x72         
		self.KXCNL_TIM2_2_H                                       = 0x73         
		self.KXCNL_TIM1_2_L                                       = 0x74         
		self.KXCNL_TIM1_2_H                                       = 0x75         
		self.KXCNL_THRS2_2                                        = 0x76         
		self.KXCNL_THRS1_2                                        = 0x77         
		self.KXCNL_DES2                                           = 0x78         
		self.KXCNL_SA2                                            = 0x79         
		self.KXCNL_MA2                                            = 0x7A         
		self.KXCNL_SETT2                                          = 0x7B         
		self.KXCNL_PPRP2                                          = 0x7C         
		self.KXCNL_TC2_L                                          = 0x7D         
		self.KXCNL_TC2_H                                          = 0x7E         
		self.KXCNL_OUTS2                                          = 0x7F         
class bits(register_base):
	def __init__(self):
		self.KXCNL_WIA_WIA_ID                                     = (0x0B << 0)  # WHO_AM_I -value
		self.KXCNL_STAT_LONG                                      = (0x01 << 7)  # is the long counter interrupt and is common to both State Programs
		self.KXCNL_STAT_SYNCW                                     = (0x01 << 6)  # provides common information for OUTW host action waiting
		self.KXCNL_STAT_SYNC1                                     = (0x01 << 5)  # reports the synchronization status of State Program 1.
		self.KXCNL_STAT_SYNC2                                     = (0x01 << 4)  # reports the synchronization status of State Program 2.
		self.KXCNL_STAT_INT_SM1                                   = (0x01 << 3)  # reports the interrupt status of State Program 1
		self.KXCNL_STAT_INT_SM2                                   = (0x01 << 2)  # reports the interrupt status of State Program 2.
		self.KXCNL_STAT_DOR                                       = (0x01 << 1)  # reports a data overrun condition
		self.KXCNL_STAT_DRDY                                      = (0x01 << 0)  # reports the data ready condition
		self.KXCNL_CNTL1_PC                                       = (0x01 << 7)  # controls the operating mode of the KXCNL.
		self.KXCNL_CNTL1_SC_2G                                    = (0x00 << 5)  # 2g
		self.KXCNL_CNTL1_SC_4G                                    = (0x01 << 5)  # 4g
		self.KXCNL_CNTL1_SC_6G                                    = (0x02 << 5)  # 6g
		self.KXCNL_CNTL1_SC_8G                                    = (0x03 << 5)  # 8g
		self.KXCNL_CNTL1_ODR_3P125                                = (0x00 << 2)  # 3.125Hz
		self.KXCNL_CNTL1_ODR_6P25                                 = (0x01 << 2)  # 6.25Hz
		self.KXCNL_CNTL1_ODR_12P5                                 = (0x02 << 2)  # 12.5Hz
		self.KXCNL_CNTL1_ODR_25                                   = (0x03 << 2)  # 25Hz
		self.KXCNL_CNTL1_ODR_50                                   = (0x04 << 2)  # 50Hz
		self.KXCNL_CNTL1_ODR_100                                  = (0x05 << 2)  # 100Hz
		self.KXCNL_CNTL1_ODR_400                                  = (0x06 << 2)  # 400Hz
		self.KXCNL_CNTL1_ODR_1600                                 = (0x07 << 2)  # 1600Hz
		self.KXCNL_CNTL1_DEBUG                                    = (0x01 << 1)  # controls the State Program Step Debug mode
		self.KXCNL_CNTL1_IEN                                      = (0x01 << 0)  # is the main interrupt enable switch
		self.KXCNL_CNTL2_SM1_PIN                                  = (0x01 << 3)  # controls the routing of the State Program 1 interrupt.
		self.KXCNL_CNTL2_SM1_EN                                   = (0x01 << 0)  # enables State Program 1.
		self.KXCNL_CNTL3_SM2_PIN                                  = (0x01 << 3)  # controls the routing of the State Program 1 interrupt.
		self.KXCNL_CNTL3_SM2_EN                                   = (0x01 << 0)  # enables State Program 1.
		self.KXCNL_CNTL4_DR_EN                                    = (0x01 << 7)  # sends the data ready signal (DRDY) to the INT1 pin.
		self.KXCNL_CNTL4_IEA                                      = (0x01 << 6)  # controls the polarity of interrupt signals
		self.KXCNL_CNTL4_IEL                                      = (0x01 << 5)  # controls the latching state of interrupt signals
		self.KXCNL_CNTL4_INT2_EN                                  = (0x01 << 4)  # enables the INT2 pin.
		self.KXCNL_CNTL4_INT1_EN                                  = (0x01 << 3)  # enables the INT1/DRDY pin.
		self.KXCNL_CNTL4_VFILT                                    = (0x01 << 2)  # enables or disables the Vector Filter
		self.KXCNL_CNTL4_STP                                      = (0x01 << 1)  # controls the activation of self test
		self.KXCNL_CNTL4_STRT                                     = (0x01 << 0)  # performs a Soft Reset
		self.KXCNL_ST1_1_RESET_NOP                                = (0x00 << 4)  
		self.KXCNL_ST1_1_RESET_TI1                                = (0x01 << 4)  
		self.KXCNL_ST1_1_RESET_TI2                                = (0x02 << 4)  
		self.KXCNL_ST1_1_RESET_TI3                                = (0x03 << 4)  
		self.KXCNL_ST1_1_RESET_TI4                                = (0x04 << 4)  
		self.KXCNL_ST1_1_RESET_GNTH1                              = (0x05 << 4)  
		self.KXCNL_ST1_1_RESET_GNTH2                              = (0x06 << 4)  
		self.KXCNL_ST1_1_RESET_LNTH1                              = (0x07 << 4)  
		self.KXCNL_ST1_1_RESET_LNTH2                              = (0x08 << 4)  
		self.KXCNL_ST1_1_RESET_GTTH1                              = (0x09 << 4)  
		self.KXCNL_ST1_1_RESET_LLTH2                              = (0x0A << 4)  
		self.KXCNL_ST1_1_RESET_GRTH1                              = (0x0B << 4)  
		self.KXCNL_ST1_1_RESET_LRTH1                              = (0x0C << 4)  
		self.KXCNL_ST1_1_RESET_GRTH2                              = (0x0D << 4)  
		self.KXCNL_ST1_1_RESET_LRTH2                              = (0x0E << 4)  
		self.KXCNL_ST1_1_RESET_NZERO                              = (0x0F << 4)  
		self.KXCNL_ST1_1_NEXT_NOP                                 = (0x00 << 0)  
		self.KXCNL_ST1_1_NEXT_TI1                                 = (0x01 << 0)  
		self.KXCNL_ST1_1_NEXT_TI2                                 = (0x02 << 0)  
		self.KXCNL_ST1_1_NEXT_TI3                                 = (0x03 << 0)  
		self.KXCNL_ST1_1_NEXT_TI4                                 = (0x04 << 0)  
		self.KXCNL_ST1_1_NEXT_GNTH1                               = (0x05 << 0)  
		self.KXCNL_ST1_1_NEXT_GNTH2                               = (0x06 << 0)  
		self.KXCNL_ST1_1_NEXT_LNTH1                               = (0x07 << 0)  
		self.KXCNL_ST1_1_NEXT_LNTH2                               = (0x08 << 0)  
		self.KXCNL_ST1_1_NEXT_GTTH1                               = (0x09 << 0)  
		self.KXCNL_ST1_1_NEXT_LLTH2                               = (0x0A << 0)  
		self.KXCNL_ST1_1_NEXT_GRTH1                               = (0x0B << 0)  
		self.KXCNL_ST1_1_NEXT_LRTH1                               = (0x0C << 0)  
		self.KXCNL_ST1_1_NEXT_GRTH2                               = (0x0D << 0)  
		self.KXCNL_ST1_1_NEXT_LRTH2                               = (0x0E << 0)  
		self.KXCNL_ST1_1_NEXT_NZERO                               = (0x0F << 0)  
		self.KXCNL_SA1_P_X                                        = (0x01 << 7)  
		self.KXCNL_SA1_N_X                                        = (0x01 << 6)  
		self.KXCNL_SA1_P_Y                                        = (0x01 << 5)  
		self.KXCNL_SA1_N_Y                                        = (0x01 << 4)  
		self.KXCNL_SA1_P_Z                                        = (0x01 << 3)  
		self.KXCNL_SA1_N_Z                                        = (0x01 << 2)  
		self.KXCNL_SA1_P_V                                        = (0x01 << 1)  
		self.KXCNL_SA1_N_V                                        = (0x01 << 0)  
		self.KXCNL_MA1_P_X                                        = (0x01 << 7)  
		self.KXCNL_MA1_N_X                                        = (0x01 << 6)  
		self.KXCNL_MA1_P_Y                                        = (0x01 << 5)  
		self.KXCNL_MA1_N_Y                                        = (0x01 << 4)  
		self.KXCNL_MA1_P_Z                                        = (0x01 << 3)  
		self.KXCNL_MA1_N_Z                                        = (0x01 << 2)  
		self.KXCNL_MA1_P_V                                        = (0x01 << 1)  
		self.KXCNL_MA1_N_V                                        = (0x01 << 0)  
		self.KXCNL_SETT1_P_DET                                    = (0x01 << 7)  
		self.KXCNL_SETT1_THR3_SA                                  = (0x01 << 6)  
		self.KXCNL_SETT1_ABS_UNSIGNED                             = (0x00 << 5)  
		self.KXCNL_SETT1_ABS_SIGNED                               = (0x01 << 5)  
		self.KXCNL_SETT1_ABS                                      = (0x01 << 5)  
		self.KXCNL_SETT1_THR3_MA                                  = (0x01 << 2)  
		self.KXCNL_SETT1_R_TAM                                    = (0x01 << 1)  
		self.KXCNL_SETT1_SITR                                     = (0x01 << 0)  
		self.KXCNL_OUTS1_P_X                                      = (0x01 << 7)  
		self.KXCNL_OUTS1_N_X                                      = (0x01 << 6)  
		self.KXCNL_OUTS1_P_Y                                      = (0x01 << 5)  
		self.KXCNL_OUTS1_N_Y                                      = (0x01 << 4)  
		self.KXCNL_OUTS1_P_Z                                      = (0x01 << 3)  
		self.KXCNL_OUTS1_N_Z                                      = (0x01 << 2)  
		self.KXCNL_OUTS1_P_V                                      = (0x01 << 1)  
		self.KXCNL_OUTS1_N_V                                      = (0x01 << 0)  
		self.KXCNL_SA2_P_X                                        = (0x01 << 7)  
		self.KXCNL_SA2_N_X                                        = (0x01 << 6)  
		self.KXCNL_SA2_P_Y                                        = (0x01 << 5)  
		self.KXCNL_SA2_N_Y                                        = (0x01 << 4)  
		self.KXCNL_SA2_P_Z                                        = (0x01 << 3)  
		self.KXCNL_SA2_N_Z                                        = (0x01 << 2)  
		self.KXCNL_SA2_P_V                                        = (0x01 << 1)  
		self.KXCNL_SA2_N_V                                        = (0x01 << 0)  
		self.KXCNL_MA2_P_X                                        = (0x01 << 7)  
		self.KXCNL_MA2_N_X                                        = (0x01 << 6)  
		self.KXCNL_MA2_P_Y                                        = (0x01 << 5)  
		self.KXCNL_MA2_N_Y                                        = (0x01 << 4)  
		self.KXCNL_MA2_P_Z                                        = (0x01 << 3)  
		self.KXCNL_MA2_N_Z                                        = (0x01 << 2)  
		self.KXCNL_MA2_P_V                                        = (0x01 << 1)  
		self.KXCNL_MA2_N_V                                        = (0x01 << 0)  
		self.KXCNL_SETT2_P_DET                                    = (0x01 << 7)  
		self.KXCNL_SETT2_THR3_SA                                  = (0x01 << 6)  
		self.KXCNL_SETT2_ABS_UNSIGNED                             = (0x00 << 5)  
		self.KXCNL_SETT2_ABS_SIGNED                               = (0x01 << 5)  
		self.KXCNL_SETT2_ABS                                      = (0x01 << 5)  
		self.KXCNL_SETT2_RADI                                     = (0x01 << 4)  
		self.KXCNL_SETT2_D_CS                                     = (0x01 << 3)  
		self.KXCNL_SETT2_THR3_MA                                  = (0x01 << 2)  
		self.KXCNL_SETT2_R_TAM                                    = (0x01 << 1)  
		self.KXCNL_SETT2_SITR                                     = (0x01 << 0)  
		self.KXCNL_OUTS2_P_X                                      = (0x01 << 7)  
		self.KXCNL_OUTS2_N_X                                      = (0x01 << 6)  
		self.KXCNL_OUTS2_P_Y                                      = (0x01 << 5)  
		self.KXCNL_OUTS2_N_Y                                      = (0x01 << 4)  
		self.KXCNL_OUTS2_P_Z                                      = (0x01 << 3)  
		self.KXCNL_OUTS2_N_Z                                      = (0x01 << 2)  
		self.KXCNL_OUTS2_P_V                                      = (0x01 << 1)  
		self.KXCNL_OUTS2_N_V                                      = (0x01 << 0)  
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KXCNL_ST1_1_NEXT={
			'GNTH1':_b.KXCNL_ST1_1_NEXT_GNTH1,
			'GNTH2':_b.KXCNL_ST1_1_NEXT_GNTH2,
			'LNTH1':_b.KXCNL_ST1_1_NEXT_LNTH1,
			'LLTH2':_b.KXCNL_ST1_1_NEXT_LLTH2,
			'TI4':_b.KXCNL_ST1_1_NEXT_TI4,
			'LRTH2':_b.KXCNL_ST1_1_NEXT_LRTH2,
			'LRTH1':_b.KXCNL_ST1_1_NEXT_LRTH1,
			'TI1':_b.KXCNL_ST1_1_NEXT_TI1,
			'TI2':_b.KXCNL_ST1_1_NEXT_TI2,
			'TI3':_b.KXCNL_ST1_1_NEXT_TI3,
			'NZERO':_b.KXCNL_ST1_1_NEXT_NZERO,
			'GTTH1':_b.KXCNL_ST1_1_NEXT_GTTH1,
			'LNTH2':_b.KXCNL_ST1_1_NEXT_LNTH2,
			'GRTH2':_b.KXCNL_ST1_1_NEXT_GRTH2,
			'NOP':_b.KXCNL_ST1_1_NEXT_NOP,
			'GRTH1':_b.KXCNL_ST1_1_NEXT_GRTH1,
		}
		self.KXCNL_ST1_1_RESET={
			'GNTH1':_b.KXCNL_ST1_1_RESET_GNTH1,
			'GNTH2':_b.KXCNL_ST1_1_RESET_GNTH2,
			'LNTH1':_b.KXCNL_ST1_1_RESET_LNTH1,
			'LLTH2':_b.KXCNL_ST1_1_RESET_LLTH2,
			'TI4':_b.KXCNL_ST1_1_RESET_TI4,
			'LRTH2':_b.KXCNL_ST1_1_RESET_LRTH2,
			'LRTH1':_b.KXCNL_ST1_1_RESET_LRTH1,
			'TI1':_b.KXCNL_ST1_1_RESET_TI1,
			'TI2':_b.KXCNL_ST1_1_RESET_TI2,
			'TI3':_b.KXCNL_ST1_1_RESET_TI3,
			'NZERO':_b.KXCNL_ST1_1_RESET_NZERO,
			'GTTH1':_b.KXCNL_ST1_1_RESET_GTTH1,
			'LNTH2':_b.KXCNL_ST1_1_RESET_LNTH2,
			'GRTH2':_b.KXCNL_ST1_1_RESET_GRTH2,
			'NOP':_b.KXCNL_ST1_1_RESET_NOP,
			'GRTH1':_b.KXCNL_ST1_1_RESET_GRTH1,
		}
		self.KXCNL_SETT2_ABS={
			'UNSIGNED':_b.KXCNL_SETT2_ABS_UNSIGNED,
			'SIGNED':_b.KXCNL_SETT2_ABS_SIGNED,
		}
		self.KXCNL_CNTL1_ODR={
			'25':_b.KXCNL_CNTL1_ODR_25,
			'12P5':_b.KXCNL_CNTL1_ODR_12P5,
			'1600':_b.KXCNL_CNTL1_ODR_1600,
			'50':_b.KXCNL_CNTL1_ODR_50,
			'3P125':_b.KXCNL_CNTL1_ODR_3P125,
			'400':_b.KXCNL_CNTL1_ODR_400,
			'100':_b.KXCNL_CNTL1_ODR_100,
			'6P25':_b.KXCNL_CNTL1_ODR_6P25,
		}
		self.KXCNL_SETT1_ABS={
			'UNSIGNED':_b.KXCNL_SETT1_ABS_UNSIGNED,
			'SIGNED':_b.KXCNL_SETT1_ABS_SIGNED,
		}
		self.KXCNL_CNTL1_SC={
			'4G':_b.KXCNL_CNTL1_SC_4G,
			'2G':_b.KXCNL_CNTL1_SC_2G,
			'8G':_b.KXCNL_CNTL1_SC_8G,
			'6G':_b.KXCNL_CNTL1_SC_6G,
		}
class masks(register_base):
	def __init__(self):
		self.KXCNL_WIA_WIA_MASK                                   = 0xFF         
		self.KXCNL_CNTL1_SC_MASK                                  = 0x60         # sets the g-range for the accelerometer outputs
		self.KXCNL_CNTL1_ODR_MASK                                 = 0x1C         # sets the output data rate for the accelerometer outputs
		self.KXCNL_CNTL2_HYST1_MASK                               = 0xE0         # sets the (unsigned) hysteresis limit
		self.KXCNL_CNTL3_HYST2_MASK                               = 0xE0         # sets the (unsigned) hysteresis limit
		self.KXCNL_ST1_1_RESET_MASK                               = 0xF0         
		self.KXCNL_ST1_1_NEXT_MASK                                = 0x0F         
		self.KXCNL_SETT1_ABS_MASK                                 = 0x20         
		self.KXCNL_PPRP1_RESET_POINT_MASK                         = 0xF0         
		self.KXCNL_PPRP1_PROGRAM_COUNTER_MASK                     = 0x0F         
		self.KXCNL_SETT2_ABS_MASK                                 = 0x20         
		self.KXCNL_PPRP2_RESET_POINT_MASK                         = 0xF0         
		self.KXCNL_PPRP2_PROGRAM_COUNTER_MASK                     = 0x0F         