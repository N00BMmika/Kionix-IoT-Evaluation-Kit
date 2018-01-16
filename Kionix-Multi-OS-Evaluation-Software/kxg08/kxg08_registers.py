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
		self.KXG08_TEMP_OUT_L                                     = 0x00         
		self.KXG08_TEMP_OUT_H                                     = 0x01         
		self.KXG08_GYRO_XOUT_L                                    = 0x02         
		self.KXG08_GYRO_XOUT_H                                    = 0x03         
		self.KXG08_GYRO_YOUT_L                                    = 0x04         
		self.KXG08_GYRO_YOUT_H                                    = 0x05         
		self.KXG08_GYRO_ZOUT_L                                    = 0x06         
		self.KXG08_GYRO_ZOUT_H                                    = 0x07         
		self.KXG08_ACCEL_XOUT_L                                   = 0x08         
		self.KXG08_ACCEL_XOUT_H                                   = 0x09         
		self.KXG08_ACCEL_YOUT_L                                   = 0x0A         
		self.KXG08_ACCEL_YOUT_H                                   = 0x0B         
		self.KXG08_ACCEL_ZOUT_L                                   = 0x0C         
		self.KXG08_ACCEL_ZOUT_H                                   = 0x0D         
		self.KXG08_AUX1_OUT_1                                     = 0x0E         # Auxiliary Sensor #1 output data bytes AUX1_OUT1 through AUX1_OUT6
		self.KXG08_AUX1_OUT_2                                     = 0x0F         
		self.KXG08_AUX1_OUT_3                                     = 0x10         
		self.KXG08_AUX1_OUT_4                                     = 0x11         
		self.KXG08_AUX1_OUT_5                                     = 0x12         
		self.KXG08_AUX1_OUT_6                                     = 0x13         
		self.KXG08_AUX2_OUT_1                                     = 0x14         # Auxiliary Sensor #2 output data bytes AUX2_OUT1 through AUX2_OUT6
		self.KXG08_AUX2_OUT_2                                     = 0x15         
		self.KXG08_AUX2_OUT_3                                     = 0x16         
		self.KXG08_AUX2_OUT_4                                     = 0x17         
		self.KXG08_AUX2_OUT_5                                     = 0x18         
		self.KXG08_AUX2_OUT_6                                     = 0x19         
		self.KXG08_TIMESTAMP7_0                                   = 0x1A         
		self.KXG08_TIMESTAMP15_8                                  = 0x1B         
		self.KXG08_TIMESTAMP18_16                                 = 0x1C         
		self.KXG08_BUF_PAST                                       = 0x1D         
		self.KXG08_BUF_SMPLEV_L                                   = 0x1E         # Reports the number of data packets (ODR cycles) currently stored in the buffer.
		self.KXG08_BUF_SMPLEV_H                                   = 0x1F         
		self.KXG08_TSCP                                           = 0x20         # Current Tilt Position Register.
		self.KXG08_TSPP                                           = 0x21         # Previous Tilt Positon Register.
		self.KXG08_AUX_STATUS                                     = 0x22         # Reports the status of Auxiliary Sensors AUX1 and AUX2.
		self.KXG08_WHO_AM_I                                       = 0x23         # WHO_AM_I
		self.KXG08_SN7_0                                          = 0x24         # Individual Identification (serial number).
		self.KXG08_SN15_8                                         = 0x25         
		self.KXG08_SN23_16                                        = 0x26         
		self.KXG08_SN31_24                                        = 0x27         
		self.KXG08_STATUS1                                        = 0x30         # Status register 1
		self.KXG08_INT1_SRC1                                      = 0x31         # Interrupt 1 source register 1
		self.KXG08_INT1_SRC2                                      = 0x32         # Interrupt 1 source register 2 (WUF direction)
		self.KXG08_INT1_SRC3                                      = 0x33         # Interrupt 1 source register 3 (Double Tap direction)
		self.KXG08_INT1_SRC4                                      = 0x34         # Interrupt 1 source register 4
		self.KXG08_INT1_L                                         = 0x35         # Reading this register releases int1 source registers
		self.KXG08_STATUS2                                        = 0x36         # Status register 2
		self.KXG08_INT2_SRC1                                      = 0x37         # Interrupt 2 source register 1
		self.KXG08_INT2_SRC2                                      = 0x38         # Interrupt 2 source register 2 (WUF direction)
		self.KXG08_INT2_SRC3                                      = 0x39         # Interrupt 2 source register 3 (Double Tap direction)
		self.KXG08_INT2_SRC4                                      = 0x3A         # Interrupt 2 source register 4
		self.KXG08_INT2_L                                         = 0x3B         # Reading this register releases int2 source registers
		self.KXG08_ACCEL_ODR                                      = 0x3C         # Accelerometer Control register
		self.KXG08_ACCEL_CTL                                      = 0x3D         # Accelerometer range control register
		self.KXG08_GYRO_ODR                                       = 0x3E         # Gyroscope Control register
		self.KXG08_GYRO_CTL                                       = 0x3F         # Gyro range control register.
		self.KXG08_INT_PIN_CTL                                    = 0x40         # This register controls the settings for the physical interrupt pins INT1 and INT2
		self.KXG08_INT_PIN_SEL1                                   = 0x41         # Physical interrupt pin INT1 select register.
		self.KXG08_INT_PIN_SEL2                                   = 0x42         # Physical interrupt pin INT2 select register.
		self.KXG08_INT_PIN_SEL3                                   = 0x43         # Physical interrupt pin select register
		self.KXG08_INT_MASK1                                      = 0x44         # Buffer Full Interrupt enable/mask bit.
		self.KXG08_INT_MASK2                                      = 0x45         # which axis and direction of detected motion can cause an interrupt.
		self.KXG08_INT_MASK3                                      = 0x46         # This register controls which axis and direction of tap/double tap can cause an interrupt.
		self.KXG08_INT_MASK4                                      = 0x47         # This register controls which axis and direction of tilt position can cause an interrupt
		self.KXG08_FSYNC_CTL                                      = 0x48         # External Synchronous control register.
		self.KXG08_BTS_TH                                         = 0x49         # This register sets the threshold for Back-to-sleep (motion detect) interrupt.
		self.KXG08_BTSWUF_TH                                      = 0x4A         # This register contains additional bits for BTS and WUF threshold.
		self.KXG08_WUF_TH                                         = 0x4B         # This register sets the Active Threshold for wake-up (motion detect) interrupt.
		self.KXG08_BTS_COUNTER                                    = 0x4C         # This register sets the time motion must be present before a wake-up interrupt is set.
		self.KXG08_WUF_COUNTER                                    = 0x4D         # This register sets the time motion must be present before a Back-to-sleep interrupt is set.
		self.KXG08_WAKE_SLEEP_CTL1                                = 0x4E         # Wake and Sleep control register 1.
		self.KXG08_WAKE_SLEEP_CTL2                                = 0x4F         # WUF and BTS threshold mode.
		self.KXG08_AUX_I2C_CTL_REG                                = 0x50         # Read/Write control register
		self.KXG08_AUX_I2C_SAD1                                   = 0x51         # Read/Write that should be used to store the SAD for auxiliary I2C device 1.
		self.KXG08_AUX_I2C_REG1                                   = 0x52         # Read/Write that should be used to store the starting data register address for auxiliary I2C device 1.
		self.KXG08_AUX_I2C_CTL1                                   = 0x53         # Register address for enable/disable control register for auxiliary I2C device 1.
		self.KXG08_AUX_I2C_BIT1                                   = 0x54         # Defines bits to toggle in the control register for auxiliary I2C device 1.
		self.KXG08_AUX_I2C_ODR                                    = 0x55         # Defines register read controls for auxiliary I2C device.
		self.KXG08_AUX_I2C_SAD2                                   = 0x56         # Read/Write that should be used to store the SAD for auxiliary I2C device 2.
		self.KXG08_AUX_I2C_REG2                                   = 0x57         # Read/Write that should be used to store the starting data register address for auxiliary I2C device 2.
		self.KXG08_AUX_I2C_CTL2                                   = 0x58         # Register address for enable/disable control register for auxiliary I2C device 2.
		self.KXG08_AUX_I2C_BIT2                                   = 0x59         # Defines bits to toggle in the control register for auxiliary I2C device 2.
		self.KXG08_AUX_I2C_ODR2                                   = 0x5A         # Defines register read controls for auxiliary I2C device.
		self.KXG08_HYST_SET                                       = 0x5B         # This register sets the Hysteresis that is placed in between the Screen Rotation states.
		self.KXG08_TILT_ANGLE_HL                                  = 0x5C         # This register sets the high level threshold for tilt angle detection.
		self.KXG08_TILT_ANGLE_LL                                  = 0x5D         # This register sets the high level threshold for tilt angle detection.
		self.KXG08_TILT_TIMER                                     = 0x5E         # This register sets the high level threshold for tilt angle detection.
		self.KXG08_TILT_TAP_ODR                                   = 0x5F         # This register sets the high level threshold for tilt angle detection.
		self.KXG08_TDTRC                                          = 0x60         # This register is responsible for enabling/disabling reporting of Tap/Double Tap
		self.KXG08_TDTC                                           = 0x61         # This register contains counter information for the detection of a double tap event.
		self.KXG08_TTH                                            = 0x62         # This register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KXG08_TTL                                            = 0x63         # This register represents the 8-bit (0d 255d) jerk low threshold to determine if a tap is detected.
		self.KXG08_FTD                                            = 0x64         # This register contains counter information for the detection of any tap event.
		self.KXG08_STD                                            = 0x65         # This register contains counter information for the detection of a double tap event.
		self.KXG08_TLT                                            = 0x66         # This register contains counter information for the detection of a tap event.
		self.KXG08_TWS                                            = 0x67         # This register contains counter information for the detection of single and double taps.
		self.KXG08_FFTH                                           = 0x68         # Free Fall Threshold
		self.KXG08_FFC                                            = 0x69         # Free Fall Counter
		self.KXG08_FFCTL                                          = 0x6A         # Free Fall Control
		self.KXG08_CTL_REG_1                                      = 0x6B         # Special control register 1
		self.KXG08_STDBY                                          = 0x6E         # Stand-by and operational control register.
		self.KXG08_BUF_WMITH_L                                    = 0x72         # Read/write control register that controls the buffer sample threshold.
		self.KXG08_BUF_WMITH_H                                    = 0x73         # Read/write control register that controls the buffer sample threshold.
		self.KXG08_BUF_TRIGTH_L                                   = 0x74         # Buffer Trigger mode threshold L
		self.KXG08_BUF_TRIGTH_H                                   = 0x75         # Buffer Trigger mode threshold H
		self.KXG08_BUF_CTL1                                       = 0x76         # Read/write control register that controls sample buffer input
		self.KXG08_BUF_CTL2                                       = 0x77         # Read/write control register that controls aux1 and aux2 buffer input
		self.KXG08_BUF_EN                                         = 0x78         # Read/write control register that controls sample buffer operation
		self.KXG08_BUF_STATUS                                     = 0x79         # reports the status of the buffers trigger function if this mode has been selected.
		self.KXG08_BUF_CLEAR                                      = 0x7A         # Latched buffer status information and the entire buffer contents are cleared when a non-zero value is written to this register
		self.KXG08_BUF_READ                                       = 0x7B         # Data in the buffer can be read by executing this command.
		self.KXG08_2080_WHO_AM_I                                  = 0x23         # WHO_AM_I
		self.KXG07_1080_WHO_AM_I                                  = 0x23         # WHO_AM_I
		self.KXG07_2080_WHO_AM_I                                  = 0x23         # WHO_AM_I
		self.KXG07_3001_WHO_AM_I                                  = 0x23         # WHO_AM_I
class bits(register_base):
	def __init__(self):
		self.KXG08_TSCP_LE                                        = (0x01 << 5)  # x-left
		self.KXG08_TSCP_RI                                        = (0x01 << 4)  # x+right
		self.KXG08_TSCP_DO                                        = (0x01 << 3)  # y-down
		self.KXG08_TSCP_UP                                        = (0x01 << 2)  # y+up
		self.KXG08_TSCP_FD                                        = (0x01 << 1)  # z-facedown
		self.KXG08_TSCP_FU                                        = (0x01 << 0)  # z+faceup
		self.KXG08_TSPP_LE                                        = (0x01 << 5)  # x-left
		self.KXG08_TSPP_RI                                        = (0x01 << 4)  # x+right
		self.KXG08_TSPP_DO                                        = (0x01 << 3)  # y-down
		self.KXG08_TSPP_UP                                        = (0x01 << 2)  # y+up
		self.KXG08_TSPP_FD                                        = (0x01 << 1)  # z-facedown
		self.KXG08_TSPP_FU                                        = (0x01 << 0)  # z+faceup
		self.KXG08_AUX_STATUS_AUX1ST_DISABLED                     = (0x00 << 0)  # Aux1 sensor is disabled
		self.KXG08_AUX_STATUS_AUX1ST_WAITING_TO_BE_ENABLED        = (0x01 << 0)  # Aux1 sensor is waiting to be enabled.
		self.KXG08_AUX_STATUS_AUX1ST_WAITING_TO_BE_DISABLED       = (0x02 << 0)  # Aux1 sensor is waiting to be disabled.
		self.KXG08_AUX_STATUS_AUX1ST_SENSOR_RUNNING               = (0x03 << 0)  # Aux1 sensor is running.
		self.KXG08_AUX_STATUS_AUX1ERR                             = (0x01 << 2)  # Aux1 data read error flag.
		self.KXG08_AUX_STATUS_AUX1FAIL                            = (0x01 << 3)  # Aux1 command sequence failure flag.
		self.KXG08_AUX_STATUS_AUX2ST_DISABLED                     = (0x00 << 4)  # Aux2 sensor is disabled
		self.KXG08_AUX_STATUS_AUX2ST_WAITING_TO_BE_ENABLED        = (0x01 << 4)  # Aux2 sensor is waiting to be enabled.
		self.KXG08_AUX_STATUS_AUX2ST_WAITING_TO_BE_DISABLED       = (0x02 << 4)  # Aux2 sensor is waiting to be disabled.
		self.KXG08_AUX_STATUS_AUX2ST_SENSOR_RUNNING               = (0x03 << 4)  # Aux2 sensor is running.
		self.KXG08_AUX_STATUS_AUX2ERR                             = (0x01 << 6)  # Aux1 data read error flag.
		self.KXG08_AUX_STATUS_AUX2FAIL                            = (0x01 << 7)  # Aux1 command sequence failure flag.
		self.KXG08_WHO_AM_I_WIA_ID                                = (0x2A << 0)  # WHO_AM_I -value 1080 version
		self.KXG08_STATUS1_INT1                                   = (0x01 << 7)  # Reports logical OR of non-masked interrupt sources sent to INT1
		self.KXG08_STATUS1_POR                                    = (0x01 << 6)  # Reset indicator.
		self.KXG08_STATUS1_AUX2_ACT                               = (0x01 << 5)  # Auxiliary sensor #2 active flag.
		self.KXG08_STATUS1_AUX1_ACT                               = (0x01 << 4)  # Auxiliary sensor #1 active flag.
		self.KXG08_STATUS1_AUX_ERR                                = (0x01 << 3)  # Auxiliary communication error
		self.KXG08_STATUS1_WAKE_SLEEP_SLEEP_MODE                  = (0x00 << 2)  # Sleep mode status
		self.KXG08_STATUS1_WAKE_SLEEP_WAKE_MODE                   = (0x01 << 2)  # Wake mode status
		self.KXG08_STATUS1_WAKE_SLEEP                             = (0x01 << 2)  # Wake/sleep status flag
		self.KXG08_STATUS1_GYRO_RUN                               = (0x01 << 0)  # Gyro's start status
		self.KXG08_INT1_SRC1_INT1_BFI                             = (0x01 << 7)  # Buffer full interrupt.
		self.KXG08_INT1_SRC1_INT1_WMI                             = (0x01 << 6)  # Buffer water mark interrupt.
		self.KXG08_INT1_SRC1_INT1_WUFS                            = (0x01 << 5)  # Wake up function interrupt.
		self.KXG08_INT1_SRC1_INT1_BTS                             = (0x01 << 4)  # Back to sleep interrupt.
		self.KXG08_INT1_SRC1_INT1_DRDY_AUX2                       = (0x01 << 3)  # Aux2 data ready interrupt.
		self.KXG08_INT1_SRC1_INT1_DRDY_AUX1                       = (0x01 << 2)  # Aux1 data ready interrupt.
		self.KXG08_INT1_SRC1_INT1_DRDY_ACC                        = (0x01 << 1)  # Accel data ready interrupt.
		self.KXG08_INT1_SRC1_INT1_DRDY_GYRO                       = (0x01 << 0)  # Gyro data ready interrupt.
		self.KXG08_INT1_SRC2_INT1_XNWU                            = (0x01 << 5)  # Wake up event detected on x-axis, negative direction
		self.KXG08_INT1_SRC2_INT1_XPWU                            = (0x01 << 4)  # Wake up event detected on x-axis, positive direction.
		self.KXG08_INT1_SRC2_INT1_YNWU                            = (0x01 << 3)  # Wake up event detected on y-axis, negative direction
		self.KXG08_INT1_SRC2_INT1_YPWU                            = (0x01 << 2)  # Wake up event detected on y-axis, positive direction.
		self.KXG08_INT1_SRC2_INT1_ZNWU                            = (0x01 << 1)  # Wake up event detected on z-axis, negative direction.
		self.KXG08_INT1_SRC2_INT1_ZPWU                            = (0x01 << 0)  # Wake up event detected on z-axis, positive direction.
		self.KXG08_INT1_SRC3_INT1_XTLE                            = (0x01 << 5)  # x-axis, negative direction.
		self.KXG08_INT1_SRC3_INT1_XTRI                            = (0x01 << 4)  # x-axis, positive direction.
		self.KXG08_INT1_SRC3_INT1_YTDO                            = (0x01 << 3)  # y-axis, negative direction.
		self.KXG08_INT1_SRC3_INT1_YTUP                            = (0x01 << 2)  # y-axis, positive direction.
		self.KXG08_INT1_SRC3_INT1_ZTFD                            = (0x01 << 1)  # z-axis, negative direction.
		self.KXG08_INT1_SRC3_INT1_ZTFU                            = (0x01 << 0)  # z-axis, positive direction.
		self.KXG08_INT1_SRC4_INT1_TPS                             = (0x01 << 3)  # Tilt position interrupt source
		self.KXG08_INT1_SRC4_INT1_TDTS_NOTAP                      = (0x00 << 1)  # no tap
		self.KXG08_INT1_SRC4_INT1_TDTS_SINGLE                     = (0x01 << 1)  # single tap event
		self.KXG08_INT1_SRC4_INT1_TDTS_DOUBLE                     = (0x02 << 1)  # double tap event
		self.KXG08_INT1_SRC4_INT1_FFS                             = (0x01 << 0)  # Freefall interrupt source
		self.KXG08_STATUS2_INT2                                   = (0x01 << 7)  # reports Logical OR of non-masked interrupt sources sent to INT2 pin.
		self.KXG08_STATUS2_POR                                    = (0x01 << 6)  # Reset indicator.
		self.KXG08_STATUS2_AUX2_ACT                               = (0x01 << 5)  # Auxiliary sensor #2 active flag.
		self.KXG08_STATUS2_AUX1_ACT                               = (0x01 << 4)  # Auxiliary sensor #1 active flag.
		self.KXG08_STATUS2_AUX_ERR                                = (0x01 << 3)  # Auxiliary communications error.
		self.KXG08_STATUS2_WAKE_SLEEP_SLEEP_MODE                  = (0x00 << 2)  
		self.KXG08_STATUS2_WAKE_SLEEP_WAKE_MODE                   = (0x01 << 2)  
		self.KXG08_STATUS2_WAKE_SLEEP                             = (0x01 << 2)  # Wake/sleep status flag
		self.KXG08_STATUS2_GYRO_RUN                               = (0x01 << 0)  # Gyroscope run flag.
		self.KXG08_INT2_SRC1_INT2_BFI                             = (0x01 << 7)  # Buffer full interrupt.
		self.KXG08_INT2_SRC1_INT2_WMI                             = (0x01 << 6)  # Buffer water mark interrupt.
		self.KXG08_INT2_SRC1_INT2_WUFS                            = (0x01 << 5)  # Wake-up function interrupt.
		self.KXG08_INT2_SRC1_INT2_BTS                             = (0x01 << 4)  # Back-to-sleep interrupt.
		self.KXG08_INT2_SRC1_INT2_DRDY_AUX2                       = (0x01 << 3)  # Aux2 data ready interrupt.
		self.KXG08_INT2_SRC1_INT2_DRDY_AUX1                       = (0x01 << 2)  # Aux1 data ready interrupt.
		self.KXG08_INT2_SRC1_INT2_DRDY_ACC                        = (0x01 << 1)  # Accelerometer data ready interrupt.
		self.KXG08_INT2_SRC1_INT2_DRDY_GYRO                       = (0x01 << 0)  # Gyro data ready interrupt.
		self.KXG08_INT2_SRC2_INT2_XNWU                            = (0x01 << 5)  # Wake up event detected on x-axis, negative direction
		self.KXG08_INT2_SRC2_INT2_XPWU                            = (0x01 << 4)  # Wake up event detected on x-axis, positive direction.
		self.KXG08_INT2_SRC2_INT2_YNWU                            = (0x01 << 3)  # Wake up event detected on y-axis, negative direction
		self.KXG08_INT2_SRC2_INT2_YPWU                            = (0x01 << 2)  # Wake up event detected on y-axis, positive direction.
		self.KXG08_INT2_SRC2_INT2_ZNWU                            = (0x01 << 1)  # Wake up event detected on z-axis, negative direction.
		self.KXG08_INT2_SRC2_INT2_ZPWU                            = (0x01 << 0)  # Wake up event detected on z-axis, positive direction.
		self.KXG08_INT2_SRC3_INT2_XTLE                            = (0x01 << 5)  # x-axis, negative direction
		self.KXG08_INT2_SRC3_INT2_XTRI                            = (0x01 << 4)  # x-axis, positive direction.
		self.KXG08_INT2_SRC3_INT2_YTDO                            = (0x01 << 3)  # y-axis, negative direction
		self.KXG08_INT2_SRC3_INT2_YTUP                            = (0x01 << 2)  # y-axis, positive direction
		self.KXG08_INT2_SRC3_INT2_ZTFD                            = (0x01 << 1)  # z-axis, negative direction.
		self.KXG08_INT2_SRC3_INT2_ZTFU                            = (0x01 << 0)  # z-axis, positive direction
		self.KXG08_INT2_SRC4_INT2_TPS                             = (0x01 << 3)  # Tilt position interrupt source.
		self.KXG08_INT2_SRC4_INT2_TDTS_NO_TAP_EVENT               = (0x00 << 1)  
		self.KXG08_INT2_SRC4_INT2_TDTS_SINGLE_TAP                 = (0x01 << 1)  
		self.KXG08_INT2_SRC4_INT2_TDTS_DOUBLE_TAP                 = (0x02 << 1)  
		self.KXG08_INT2_SRC4_INT2_FFS                             = (0x01 << 0)  # Free fall interrupt source.
		self.KXG08_ACCEL_ODR_LPMODEA                              = (0x01 << 7)  # Accelerometer low power mode enable
		self.KXG08_ACCEL_ODR_NAVGA_NO_AVG                         = (0x00 << 4)  # No Averaging
		self.KXG08_ACCEL_ODR_NAVGA_2_SAMPLE_AVG                   = (0x01 << 4)  # 2 Samples Averaged
		self.KXG08_ACCEL_ODR_NAVGA_4_SAMPLE_AVG                   = (0x02 << 4)  # 4 Samples Averaged
		self.KXG08_ACCEL_ODR_NAVGA_8_SAMPLE_AVG                   = (0x03 << 4)  # 8 Samples Averaged
		self.KXG08_ACCEL_ODR_NAVGA_16_SAMPLE_AVG                  = (0x04 << 4)  # 16 Samples Averaged (default)
		self.KXG08_ACCEL_ODR_NAVGA_32_SAMPLE_AVG                  = (0x05 << 4)  # 32 Samples Averaged
		self.KXG08_ACCEL_ODR_NAVGA_64_SAMPLE_AVG                  = (0x06 << 4)  # 64 Samples Averaged
		self.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG                 = (0x07 << 4)  # 128 Samples Averaged
		self.KXG08_ACCEL_ODR_ODRA_0P781                           = (0x00 << 0)  # 0.78Hz
		self.KXG08_ACCEL_ODR_ODRA_1P563                           = (0x01 << 0)  # 1.563Hz
		self.KXG08_ACCEL_ODR_ODRA_3P125                           = (0x02 << 0)  # 3.125Hz
		self.KXG08_ACCEL_ODR_ODRA_6P25                            = (0x03 << 0)  # 6.25Hz
		self.KXG08_ACCEL_ODR_ODRA_12P5                            = (0x04 << 0)  # 12.5Hz
		self.KXG08_ACCEL_ODR_ODRA_25                              = (0x05 << 0)  # 25Hz
		self.KXG08_ACCEL_ODR_ODRA_50                              = (0x06 << 0)  # 50Hz
		self.KXG08_ACCEL_ODR_ODRA_100                             = (0x07 << 0)  # 100Hz
		self.KXG08_ACCEL_ODR_ODRA_200                             = (0x08 << 0)  # 200Hz
		self.KXG08_ACCEL_ODR_ODRA_400                             = (0x09 << 0)  # 400Hz
		self.KXG08_ACCEL_ODR_ODRA_800                             = (0x0A << 0)  # 800Hz
		self.KXG08_ACCEL_ODR_ODRA_1600                            = (0x0B << 0)  # 1600Hz
		self.KXG08_ACCEL_ODR_ODRA_3200                            = (0x0C << 0)  # 3200Hz
		self.KXG08_ACCEL_ODR_ODRA_6400                            = (0x0D << 0)  # 6400Hz
		self.KXG08_ACCEL_ODR_ODRA_12800                           = (0x0E << 0)  # 12800Hz
		self.KXG08_ACCEL_ODR_ODRA_25600                           = (0x0F << 0)  # 25600Hz
		self.KXG08_ACCEL_CTL_ACC_ST_POL                           = (0x01 << 5)  # Accelerometer self test polarity control.
		self.KXG08_ACCEL_CTL_ACC_ST                               = (0x01 << 4)  # Accelerometer self test enable control.
		self.KXG08_ACCEL_CTL_ACC_BW_ODR_2                         = (0x00 << 3)  # BW = ODR/2
		self.KXG08_ACCEL_CTL_ACC_BW_ODR_8                         = (0x01 << 3)  # BW = ODR/8
		self.KXG08_ACCEL_CTL_ACC_BW                               = (0x01 << 3)  # Accelerometer bandwidth control.
		self.KXG08_ACCEL_CTL_ACC_FS_2G                            = (0x00 << 0)  
		self.KXG08_ACCEL_CTL_ACC_FS_4G                            = (0x01 << 0)  
		self.KXG08_ACCEL_CTL_ACC_FS_8G                            = (0x02 << 0)  
		self.KXG08_ACCEL_CTL_ACC_FS_16G                           = (0x03 << 0)  
		self.KXG08_GYRO_ODR_LPMODEG                               = (0x01 << 7)  # Gyroscope low power mode enable.
		self.KXG08_GYRO_ODR_NAVGG_NO_AVG                          = (0x00 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_2_SAMPLE_AVG                    = (0x01 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_4_SAMPLE_AVG                    = (0x02 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_8_SAMPLE_AVG                    = (0x03 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_16_SAMPLE_AVG                   = (0x04 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_32_SAMPLE_AVG                   = (0x05 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_64_SAMPLE_AVG                   = (0x06 << 4)  
		self.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG                  = (0x07 << 4)  
		self.KXG08_GYRO_ODR_ODRG_0P781                            = (0x00 << 0)  # 0.78Hz
		self.KXG08_GYRO_ODR_ODRG_1P563                            = (0x01 << 0)  # 1.563Hz
		self.KXG08_GYRO_ODR_ODRG_3P125                            = (0x02 << 0)  # 3.125Hz
		self.KXG08_GYRO_ODR_ODRG_6P25                             = (0x03 << 0)  # 6.25Hz
		self.KXG08_GYRO_ODR_ODRG_12P5                             = (0x04 << 0)  # 12.5Hz
		self.KXG08_GYRO_ODR_ODRG_25                               = (0x05 << 0)  # 25Hz
		self.KXG08_GYRO_ODR_ODRG_50                               = (0x06 << 0)  # 50Hz
		self.KXG08_GYRO_ODR_ODRG_100                              = (0x07 << 0)  # 100Hz
		self.KXG08_GYRO_ODR_ODRG_200                              = (0x08 << 0)  # 200Hz
		self.KXG08_GYRO_ODR_ODRG_400                              = (0x09 << 0)  # 400Hz
		self.KXG08_GYRO_ODR_ODRG_800                              = (0x0A << 0)  # 800Hz
		self.KXG08_GYRO_ODR_ODRG_1600                             = (0x0B << 0)  # 1600Hz
		self.KXG08_GYRO_ODR_ODRG_3200                             = (0x0C << 0)  # 3200Hz
		self.KXG08_GYRO_ODR_ODRG_6400                             = (0x0D << 0)  # 6400Hz
		self.KXG08_GYRO_ODR_ODRG_12800                            = (0x0E << 0)  # 12800Hz
		self.KXG08_GYRO_ODR_ODRG_12800_1                          = (0x0F << 0)  # 12800Hz
		self.KXG08_GYRO_CTL_GYRO_BW_ODR_8                         = (0x00 << 3)  # BW = ODR/8
		self.KXG08_GYRO_CTL_GYRO_BW_ODR_2                         = (0x01 << 3)  # BW = ODR/2
		self.KXG08_GYRO_CTL_GYRO_BW                               = (0x01 << 3)  
		self.KXG08_GYRO_CTL_GYRO_FS_64                            = (0x00 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_128                           = (0x01 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_256                           = (0x02 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_512                           = (0x03 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_1024                          = (0x04 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_2048                          = (0x05 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_TBD1                          = (0x06 << 0)  
		self.KXG08_GYRO_CTL_GYRO_FS_TBD2                          = (0x07 << 0)  
		self.KXG08_INT_PIN_CTL_IEN2                               = (0x01 << 7)  # Active high enable for INT2 pin.
		self.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW                    = (0x00 << 6)  
		self.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH                   = (0x01 << 6)  
		self.KXG08_INT_PIN_CTL_IEA2                               = (0x01 << 6)  # Interrupt polarity select for INT2 pin.
		self.KXG08_INT_PIN_CTL_IEL2_LATCHED                       = (0x00 << 4)  # Latched
		self.KXG08_INT_PIN_CTL_IEL2_PULSED_50US                   = (0x01 << 4)  # Pulsed 50uS
		self.KXG08_INT_PIN_CTL_IEL2_PULSED_200US                  = (0x02 << 4)  # Pulsed 200uS
		self.KXG08_INT_PIN_CTL_IEL2_REALTIME                      = (0x03 << 4)  # Realtime
		self.KXG08_INT_PIN_CTL_IEN1                               = (0x01 << 3)  # Active high enable for INT1 pin.
		self.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW                    = (0x00 << 2)  
		self.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH                   = (0x01 << 2)  
		self.KXG08_INT_PIN_CTL_IEA1                               = (0x01 << 2)  # Interrupt polarity select for INT1 pin.
		self.KXG08_INT_PIN_CTL_IEL1_LATCHED                       = (0x00 << 0)  # Latched
		self.KXG08_INT_PIN_CTL_IEL1_PULSED_50US                   = (0x01 << 0)  # Pulsed 50uS
		self.KXG08_INT_PIN_CTL_IEL1_PULSED_200US                  = (0x02 << 0)  # Pulsed 200uS
		self.KXG08_INT_PIN_CTL_IEL1_REALTIME                      = (0x03 << 0)  # Realtime
		self.KXG08_INT_PIN_SEL1_BFI_P1                            = (0x01 << 7)  # Buffer Full Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_WMI_P1                            = (0x01 << 6)  # Water Mark Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_WUF_P1                            = (0x01 << 5)  # Wake Up Function Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_BTS_P1                            = (0x01 << 4)  # Back To Sleep Function Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_DRDY_AUX2_P1                      = (0x01 << 3)  # Data Ready Aux2 Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_DRDY_AUX1_P1                      = (0x01 << 2)  # Data Ready AUX1 Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_DRDY_ACC_P1                       = (0x01 << 1)  # Data Ready Accelerometer Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL1_DRDY_GYRO_P1                      = (0x01 << 0)  # Data Ready Gyroscope Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL2_BFI_P2                            = (0x01 << 7)  # Buffer Full Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_WMI_P2                            = (0x01 << 6)  # Water Mark Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_WUF_P2                            = (0x01 << 5)  # Wake-up Function Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_BTS_P2                            = (0x01 << 4)  # Back-to-sleep Function Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_DRDY_AUX2_P2                      = (0x01 << 3)  # Data Ready Aux2 Interrupt for INT2 pin.
		self.KXG08_INT_PIN_SEL2_DRDY_AUX1_P2                      = (0x01 << 2)  # Data Ready AUX1 Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_DRDY_ACC_P2                       = (0x01 << 1)  # Data Ready Accelerometer Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL2_DRDY_GYRO_P2                      = (0x01 << 0)  # Data Ready Gyroscope Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL3_TPS_P2                            = (0x01 << 7)  # Tilt Position Interrupt for INT2 pin
		self.KXG08_INT_PIN_SEL3_TDS_P2                            = (0x01 << 5)  # Tap/Double Tap Interrupt for INT2 pin.
		self.KXG08_INT_PIN_SEL3_FFS_P2                            = (0x01 << 4)  # Free fall Interrupt for INT2 pin.
		self.KXG08_INT_PIN_SEL3_TPS_P1                            = (0x01 << 3)  # Tilt Position Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL3_TDS_P1                            = (0x01 << 1)  # Tap/Double Tap Interrupt for INT1 pin.
		self.KXG08_INT_PIN_SEL3_FFS_P1                            = (0x01 << 0)  # Free fall Interrupt for INT1 pin.
		self.KXG08_INT_MASK1_BFIE                                 = (0x01 << 7)  # Buffer Full Interrupt enable/mask bit.
		self.KXG08_INT_MASK1_WMIE                                 = (0x01 << 6)  # Water Mark Interrupt enable/mask bit.
		self.KXG08_INT_MASK1_DRDY_AUX2                            = (0x01 << 3)  # Data Ready Aux2 Interrupt enable/mask bit.
		self.KXG08_INT_MASK1_DRDY_AUX1                            = (0x01 << 2)  # Data Ready AUX1 Interrupt enable/mask bit.
		self.KXG08_INT_MASK1_DRDY_ACC                             = (0x01 << 1)  # Data Ready Accelerometer Interrupt enable/mask bit.
		self.KXG08_INT_MASK1_DRDY_GYRO                            = (0x01 << 0)  # Data Ready Gyroscope Interrupt enable/mask bit.
		self.KXG08_INT_MASK2_XNWUE                                = (0x01 << 5)  # x negative (x-) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK2_XPWUE                                = (0x01 << 4)  # x positive (x+) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK2_YNWUE                                = (0x01 << 3)  # y negative (y-) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK2_YPWUE                                = (0x01 << 2)  # y positive (y+) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK2_ZNWUE                                = (0x01 << 1)  # z negative (z-) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK2_ZPWUE                                = (0x01 << 0)  # z positive (z+) mask for WUF/BTS, 0=disable, 1=enable.
		self.KXG08_INT_MASK3_TLEM                                 = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK3_TRIM                                 = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK3_TDOM                                 = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK3_TUPM                                 = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK3_TFDM                                 = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK3_TFUM                                 = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TLEM                                 = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TRIM                                 = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TDOM                                 = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TUPM                                 = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TFDM                                 = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KXG08_INT_MASK4_TFUM                                 = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KXG08_FSYNC_CTL_FSYNC_TRIG_INT2                      = (0x00 << 6)  # INT2 = interrupt-2.
		self.KXG08_FSYNC_CTL_FSYNC_TRIG_FSYNC                     = (0x01 << 6)  # INT2 = fsync function
		self.KXG08_FSYNC_CTL_FSYNC_TRIG                           = (0x01 << 6)  # Defines INT2 and SYNC_TRIG pin functionality
		self.KXG08_FSYNC_CTL_FSYNC_MODE_DISABLED                  = (0x00 << 4)  # FSYNC is disabled. SYNC pin is tri-stated.
		self.KXG08_FSYNC_CTL_FSYNC_MODE_INPUT_EXT                 = (0x01 << 4)  # FSYNC is enabled. Sync pin is configured as input pin. Buffer is updated in sync with external clock applied at SYNC pin.
		self.KXG08_FSYNC_CTL_FSYNC_MODE_INPUT                     = (0x02 << 4)  # FSYNC is enabled. Sync pin is configured as input pin. State of SYNC pin is stored in selected sensor's LSB bit.
		self.KXG08_FSYNC_CTL_FSYNC_MODE_OUTPUT                    = (0x03 << 4)  # FSYNC is disabled. SYNC pin is configured as output pin.
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL000                     = (0x00 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL001                     = (0x01 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL010                     = (0x02 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL011                     = (0x03 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL100                     = (0x04 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL101                     = (0x05 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL110                     = (0x06 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_FSYNC_CTL_FSYNC_SEL_SEL111                     = (0x07 << 0)  # Definition according FSYNC_MODE selection
		self.KXG08_WAKE_SLEEP_CTL1_TH_MODE_ABSOLUTE_THRESHOLD     = (0x00 << 5)  # Absolute threshold. ASIC compares current output to threshold.
		self.KXG08_WAKE_SLEEP_CTL1_TH_MODE_RELATIVE_THRESHOLD     = (0x01 << 5)  # Relative threshold. ASIC compares difference between current output and previous output to threshold.
		self.KXG08_WAKE_SLEEP_CTL1_TH_MODE                        = (0x01 << 5)  
		self.KXG08_WAKE_SLEEP_CTL1_C_MODE_COUNTER_CLEAR           = (0x00 << 4)  # Counter is cleared once activity level is outside the threshold.
		self.KXG08_WAKE_SLEEP_CTL1_C_MODE_COUNTER_DECREMENT       = (0x01 << 4)  # Counter is decremented by one when activity level is outside the threshold.
		self.KXG08_WAKE_SLEEP_CTL1_C_MODE                         = (0x01 << 4)  # Defines de-bounce counter clear mode.
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_0P781                     = (0x00 << 0)  # 0.78Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_1P563                     = (0x01 << 0)  # 1.563Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_3P125                     = (0x02 << 0)  # 3.125Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_6P25                      = (0x03 << 0)  # 6.25Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_12P5                      = (0x04 << 0)  # 12.5Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_25                        = (0x05 << 0)  # 25Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_50                        = (0x06 << 0)  # 50Hz
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_100                       = (0x07 << 0)  # 100Hz
		self.KXG08_WAKE_SLEEP_CTL2_BTS_EN                         = (0x01 << 7)  # Active high back-to-sleep function enable
		self.KXG08_WAKE_SLEEP_CTL2_WUF_EN                         = (0x01 << 6)  # Active high wake-up function enable.
		self.KXG08_WAKE_SLEEP_CTL2_MAN_SLEEP                      = (0x01 << 5)  # Forces transition to sleep state.
		self.KXG08_WAKE_SLEEP_CTL2_MAN_WAKE                       = (0x01 << 4)  # Forces transition to wake state.
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_0P048828                  = (0x00 << 0)  
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_0P097656                  = (0x01 << 0)  
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_0P19531                   = (0x02 << 0)  
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_0P3906                    = (0x03 << 0)  
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_0P781                     = (0x04 << 0)  # 0.78Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_1P563                     = (0x05 << 0)  # 1.563Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_3P125                     = (0x06 << 0)  # 3.125Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_6P25                      = (0x07 << 0)  # 6.25Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_12P5                      = (0x08 << 0)  # 12.5Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_25                        = (0x09 << 0)  # 25Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_50                        = (0x0A << 0)  # 50Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_100                       = (0x0B << 0)  # 100Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_100_2                     = (0x0C << 0)  # 100Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_100_3                     = (0x0D << 0)  # 100Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_100_4                     = (0x0E << 0)  # 100Hz
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_100_5                     = (0x0F << 0)  # 100Hz
		self.KXG08_AUX_I2C_CTL_REG_AUX_CTL_POL2                   = (0x01 << 5)  # Defines control bit polarity for aux2 enable/disable command sequences.
		self.KXG08_AUX_I2C_CTL_REG_AUX_CTL_POL1                   = (0x01 << 4)  # Defines control bit polarity for aux1 enable/disable command sequences.
		self.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD_100                = (0x00 << 3)  # 100kHz
		self.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD_400                = (0x01 << 3)  # 400kHz
		self.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD                    = (0x01 << 3)  # Sets I2C bus speed.
		self.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP_DISABLED           = (0x00 << 2)  
		self.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP_ENABLED            = (0x01 << 2)  
		self.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP                    = (0x01 << 2)  # Active pullup
		self.KXG08_AUX_I2C_CTL_REG_AUX_BYPASS                     = (0x01 << 1)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_0                           = (0x00 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_1                           = (0x01 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_2                           = (0x02 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_3                           = (0x03 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_4                           = (0x04 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_5                           = (0x05 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_6                           = (0x06 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1_D_DNE                         = (0x07 << 4)  
		self.KXG08_AUX_I2C_ODR_AUX1ODR_0P781                      = (0x00 << 0)  # 0.78Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1P563                      = (0x01 << 0)  # 1.563Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_3P125                      = (0x02 << 0)  # 3.125Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_6P25                       = (0x03 << 0)  # 6.25Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_12P5                       = (0x04 << 0)  # 12.5Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_25                         = (0x05 << 0)  # 25Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_50                         = (0x06 << 0)  # 50Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_100                        = (0x07 << 0)  # 100Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_200                        = (0x08 << 0)  # 200Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_400                        = (0x09 << 0)  # 400Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_800                        = (0x0A << 0)  # 800Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1600                       = (0x0B << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1600_1                     = (0x0C << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1600_2                     = (0x0D << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1600_3                     = (0x0E << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR_AUX1ODR_1600_4                     = (0x0F << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR2_AUX2_D_0                          = (0x00 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_1                          = (0x01 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_2                          = (0x02 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_3                          = (0x03 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_4                          = (0x04 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_5                          = (0x05 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_6                          = (0x06 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2_D_DNE                        = (0x07 << 4)  
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_0P781                     = (0x00 << 0)  # 0.78Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1P563                     = (0x01 << 0)  # 1.563Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_3P125                     = (0x02 << 0)  # 3.125Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_6P25                      = (0x03 << 0)  # 6.25Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_12P5                      = (0x04 << 0)  # 12.5Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_25                        = (0x05 << 0)  # 25Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_50                        = (0x06 << 0)  # 50Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_100                       = (0x07 << 0)  # 100Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_200                       = (0x08 << 0)  # 200Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_400                       = (0x09 << 0)  # 400Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_800                       = (0x0A << 0)  # 800Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1600                      = (0x0B << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_1                    = (0x0C << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_2                    = (0x0D << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_3                    = (0x0E << 0)  # 1600Hz
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_4                    = (0x0F << 0)  # 1600Hz
		self.KXG08_TILT_TAP_ODR_OTDT_12P5                         = (0x00 << 3)  # 12.5Hz
		self.KXG08_TILT_TAP_ODR_OTDT_25                           = (0x01 << 3)  # 25Hz
		self.KXG08_TILT_TAP_ODR_OTDT_50                           = (0x02 << 3)  # 50Hz
		self.KXG08_TILT_TAP_ODR_OTDT_100                          = (0x03 << 3)  # 100Hz
		self.KXG08_TILT_TAP_ODR_OTDT_200                          = (0x04 << 3)  # 200Hz
		self.KXG08_TILT_TAP_ODR_OTDT_400                          = (0x05 << 3)  # 400Hz
		self.KXG08_TILT_TAP_ODR_OTDT_800                          = (0x06 << 3)  # 800Hz
		self.KXG08_TILT_TAP_ODR_OTDT_1600                         = (0x07 << 3)  # 1600Hz
		self.KXG08_TILT_TAP_ODR_OTP_1P563                         = (0x00 << 0)  # 1.563Hz
		self.KXG08_TILT_TAP_ODR_OTP_3P125                         = (0x01 << 0)  # 3.125Hz
		self.KXG08_TILT_TAP_ODR_OTP_6P25                          = (0x02 << 0)  # 6.25Hz
		self.KXG08_TILT_TAP_ODR_OTP_12P5                          = (0x03 << 0)  # 12.5Hz
		self.KXG08_TILT_TAP_ODR_OTP_25                            = (0x04 << 0)  # 25Hz
		self.KXG08_TILT_TAP_ODR_OTP_50                            = (0x05 << 0)  # 50Hz
		self.KXG08_TILT_TAP_ODR_OTP_50_1                          = (0x06 << 0)  # 50Hz
		self.KXG08_TILT_TAP_ODR_OTP_50_2                          = (0x07 << 0)  # 50Hz
		self.KXG08_TDTRC_DTRE                                     = (0x01 << 1)  # enables/disables the double tap interrupt
		self.KXG08_TDTRC_STRE                                     = (0x01 << 0)  # enables/disables single tap interrupt
		self.KXG08_FFCTL_FFIE                                     = (0x01 << 7)  # Free fall engine enable
		self.KXG08_FFCTL_ULMODE_LATCHED                           = (0x00 << 6)  
		self.KXG08_FFCTL_ULMODE_UNLATCHED                         = (0x01 << 6)  
		self.KXG08_FFCTL_ULMODE                                   = (0x01 << 6)  # Free fall interrupt latch/un-latch control
		self.KXG08_FFCTL_DCRM_UP_DOWN                             = (0x00 << 3)  # count up/down
		self.KXG08_FFCTL_DCRM_UP_RESET                            = (0x01 << 3)  # count up/reset
		self.KXG08_FFCTL_DCRM                                     = (0x01 << 3)  # Debounce methodology control
		self.KXG08_FFCTL_OFFI_12P5                                = (0x04 << 0)  # 12.5Hz
		self.KXG08_FFCTL_OFFI_25                                  = (0x05 << 0)  # 25Hz
		self.KXG08_FFCTL_OFFI_50                                  = (0x06 << 0)  # 50Hz
		self.KXG08_FFCTL_OFFI_100                                 = (0x07 << 0)  # 100Hz
		self.KXG08_FFCTL_OFFI_200                                 = (0x08 << 0)  # 200Hz
		self.KXG08_FFCTL_OFFI_400                                 = (0x09 << 0)  # 400Hz
		self.KXG08_FFCTL_OFFI_800                                 = (0x0A << 0)  # 800Hz
		self.KXG08_FFCTL_OFFI_1600                                = (0x0B << 0)  # 1600Hz
		self.KXG08_CTL_REG_1_SRST                                 = (0x01 << 7)  # initiates software reset, which performs the RAM reboot routine.
		self.KXG08_CTL_REG_1_TILT_EN                              = (0x01 << 3)  # Tilt position engine enable.
		self.KXG08_CTL_REG_1_TAP_EN                               = (0x01 << 2)  # Tap/Double Tap engine enable.
		self.KXG08_CTL_REG_1_CONT_TIME_EN                         = (0x01 << 0)  # Timestamp mode enable.
		self.KXG08_STDBY_I2C_DIS                                  = (0x01 << 7)  # Active high I2C disable bit
		self.KXG08_STDBY_TEMP_STDBY_ENABLED                       = (0x00 << 5)  # Temperature sensor is enabled.
		self.KXG08_STDBY_TEMP_STDBY_DISABLED                      = (0x01 << 5)  # Temperature sensor is disabled.
		self.KXG08_STDBY_TEMP_STDBY                               = (0x01 << 5)  # Active low Temperature sensor enable.
		self.KXG08_STDBY_AUX2_STDBY_ENABLED                       = (0x00 << 4)  # Aux2 sensor is enabled.
		self.KXG08_STDBY_AUX2_STDBY_DISABLED                      = (0x01 << 4)  # Aux2 sensor is disabled.
		self.KXG08_STDBY_AUX2_STDBY                               = (0x01 << 4)  # Active low aux2 sensor enable.
		self.KXG08_STDBY_AUX1_STDBY_ENABLED                       = (0x00 << 3)  # Aux1 sensor is enabled.
		self.KXG08_STDBY_AUX1_STDBY_DISABLED                      = (0x01 << 3)  # Aux1 sensor is disabled.
		self.KXG08_STDBY_AUX1_STDBY                               = (0x01 << 3)  # Active low aux1 sensor enable.
		self.KXG08_STDBY_GYRO_FSTART_DISABLED                     = (0x00 << 2)  # Gyro fast start function is disabled.
		self.KXG08_STDBY_GYRO_FSTART_ENABLED                      = (0x01 << 2)  # Gyro fast start function is enabled.
		self.KXG08_STDBY_GYRO_FSTART                              = (0x01 << 2)  # Active high gyroscope fast start sensor enable
		self.KXG08_STDBY_GYRO_STDBY_ENABLED                       = (0x00 << 1)  # Gyro sensor is enabled.
		self.KXG08_STDBY_GYRO_STDBY_DISABLED                      = (0x01 << 1)  # Gyro sensor is disabled.
		self.KXG08_STDBY_GYRO_STDBY                               = (0x01 << 1)  # Active low gyroscope sensor enable.
		self.KXG08_STDBY_ACC_STDBY_ENABLED                        = (0x00 << 0)  # Accelerometer sensor is enabled.
		self.KXG08_STDBY_ACC_STDBY_DISABLED                       = (0x01 << 0)  # Accelerometer sensor is disabled.
		self.KXG08_STDBY_ACC_STDBY                                = (0x01 << 0)  # Active low Accelerometer sensor enable.
		self.KXG08_BUF_CTL1_BUF_TEMP                              = (0x01 << 6)  
		self.KXG08_BUF_CTL1_BUF_ACC_X                             = (0x01 << 5)  
		self.KXG08_BUF_CTL1_BUF_ACC_Y                             = (0x01 << 4)  
		self.KXG08_BUF_CTL1_BUF_ACC_Z                             = (0x01 << 3)  
		self.KXG08_BUF_CTL1_BUF_GYR_X                             = (0x01 << 2)  
		self.KXG08_BUF_CTL1_BUF_GYR_Y                             = (0x01 << 1)  
		self.KXG08_BUF_CTL1_BUF_GYR_Z                             = (0x01 << 0)  
		self.KXG08_BUF_CTL2_BUF_AUX2                              = (0x01 << 1)  
		self.KXG08_BUF_CTL2_BUF_AUX1                              = (0x01 << 0)  
		self.KXG08_BUF_EN_BUFE                                    = (0x01 << 7)  # controls activation of the sample buffer.
		self.KXG08_BUF_EN_BUF_TIME_EN                             = (0x01 << 4)  # Active high buffer times stamp enable.
		self.KXG08_BUF_EN_BUF_M_FIFO                              = (0x00 << 0)  # The buffer collects 4096 bytes of data until full, collecting new data only when the buffer is not full.
		self.KXG08_BUF_EN_BUF_M_STREAM                            = (0x01 << 0)  # The buffer holds the last 4096 bytes of data. Once the buffer is full, the oldest data is discarded to make room for newer data.
		self.KXG08_BUF_EN_BUF_M_TRIGGER                           = (0x02 << 0)  # When a trigger event occurs (logic high input on TRIG pin), the buffer holds the last data set of SMP[11:0] samples
		self.KXG08_BUF_EN_BUF_M_NOT_VALID                         = (0x03 << 0)  
		self.KXG08_BUF_STATUS_BUF_TRIG                            = (0x01 << 7)  # reports the status of the buffers trigger function if this mode has been selected.
		self.KXG08_2080_WHO_AM_I_WIA_ID                           = (0x26 << 0)  # WHO_AM_I -value -2080 version
		self.KXG07_1080_WHO_AM_I_WIA_ID                           = (0x29 << 0)  # WHO_AM_I -value -1080 version
		self.KXG07_2080_WHO_AM_I_WIA_ID                           = (0x25 << 0)  # WHO_AM_I -value -2080 version
		self.KXG07_3001_WHO_AM_I_WIA_ID                           = (0x2F << 0)  # WHO_AM_I -value -3001 version
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KXG08_BUF_EN_BUF_M={
			'TRIGGER':_b.KXG08_BUF_EN_BUF_M_TRIGGER,
			'FIFO':_b.KXG08_BUF_EN_BUF_M_FIFO,
			'STREAM':_b.KXG08_BUF_EN_BUF_M_STREAM,
			'NOT_VALID':_b.KXG08_BUF_EN_BUF_M_NOT_VALID,
		}
		self.KXG08_FFCTL_ULMODE={
			'LATCHED':_b.KXG08_FFCTL_ULMODE_LATCHED,
			'UNLATCHED':_b.KXG08_FFCTL_ULMODE_UNLATCHED,
		}
		self.KXG08_STDBY_ACC_STDBY={
			'DISABLED':_b.KXG08_STDBY_ACC_STDBY_DISABLED,
			'ENABLED':_b.KXG08_STDBY_ACC_STDBY_ENABLED,
		}
		self.KXG08_WAKE_SLEEP_CTL2_OBTS={
			'0P19531':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_0P19531,
			'0P3906':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_0P3906,
			'0P781':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_0P781,
			'6P25':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_6P25,
			'25':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_25,
			'12P5':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_12P5,
			'0P048828':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_0P048828,
			'100_2':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_100_2,
			'100_5':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_100_5,
			'100_4':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_100_4,
			'50':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_50,
			'1P563':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_1P563,
			'3P125':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_3P125,
			'0P097656':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_0P097656,
			'100':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_100,
			'100_3':_b.KXG08_WAKE_SLEEP_CTL2_OBTS_100_3,
		}
		self.KXG08_GYRO_ODR_ODRG={
			'200':_b.KXG08_GYRO_ODR_ODRG_200,
			'6400':_b.KXG08_GYRO_ODR_ODRG_6400,
			'0P781':_b.KXG08_GYRO_ODR_ODRG_0P781,
			'12800_1':_b.KXG08_GYRO_ODR_ODRG_12800_1,
			'3200':_b.KXG08_GYRO_ODR_ODRG_3200,
			'12P5':_b.KXG08_GYRO_ODR_ODRG_12P5,
			'1600':_b.KXG08_GYRO_ODR_ODRG_1600,
			'50':_b.KXG08_GYRO_ODR_ODRG_50,
			'1P563':_b.KXG08_GYRO_ODR_ODRG_1P563,
			'3P125':_b.KXG08_GYRO_ODR_ODRG_3P125,
			'25':_b.KXG08_GYRO_ODR_ODRG_25,
			'12800':_b.KXG08_GYRO_ODR_ODRG_12800,
			'400':_b.KXG08_GYRO_ODR_ODRG_400,
			'100':_b.KXG08_GYRO_ODR_ODRG_100,
			'800':_b.KXG08_GYRO_ODR_ODRG_800,
			'6P25':_b.KXG08_GYRO_ODR_ODRG_6P25,
		}
		self.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD={
			'100':_b.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD_100,
			'400':_b.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD_400,
		}
		self.KXG08_STDBY_GYRO_FSTART={
			'DISABLED':_b.KXG08_STDBY_GYRO_FSTART_DISABLED,
			'ENABLED':_b.KXG08_STDBY_GYRO_FSTART_ENABLED,
		}
		self.KXG08_FFCTL_OFFI={
			'25':_b.KXG08_FFCTL_OFFI_25,
			'200':_b.KXG08_FFCTL_OFFI_200,
			'12P5':_b.KXG08_FFCTL_OFFI_12P5,
			'1600':_b.KXG08_FFCTL_OFFI_1600,
			'50':_b.KXG08_FFCTL_OFFI_50,
			'400':_b.KXG08_FFCTL_OFFI_400,
			'100':_b.KXG08_FFCTL_OFFI_100,
			'800':_b.KXG08_FFCTL_OFFI_800,
		}
		self.KXG08_ACCEL_ODR_ODRA={
			'200':_b.KXG08_ACCEL_ODR_ODRA_200,
			'6400':_b.KXG08_ACCEL_ODR_ODRA_6400,
			'0P781':_b.KXG08_ACCEL_ODR_ODRA_0P781,
			'3200':_b.KXG08_ACCEL_ODR_ODRA_3200,
			'12P5':_b.KXG08_ACCEL_ODR_ODRA_12P5,
			'1600':_b.KXG08_ACCEL_ODR_ODRA_1600,
			'50':_b.KXG08_ACCEL_ODR_ODRA_50,
			'1P563':_b.KXG08_ACCEL_ODR_ODRA_1P563,
			'25600':_b.KXG08_ACCEL_ODR_ODRA_25600,
			'3P125':_b.KXG08_ACCEL_ODR_ODRA_3P125,
			'25':_b.KXG08_ACCEL_ODR_ODRA_25,
			'12800':_b.KXG08_ACCEL_ODR_ODRA_12800,
			'400':_b.KXG08_ACCEL_ODR_ODRA_400,
			'100':_b.KXG08_ACCEL_ODR_ODRA_100,
			'800':_b.KXG08_ACCEL_ODR_ODRA_800,
			'6P25':_b.KXG08_ACCEL_ODR_ODRA_6P25,
		}
		self.KXG08_FSYNC_CTL_FSYNC_SEL={
			'SEL101':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL101,
			'SEL100':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL100,
			'SEL110':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL110,
			'SEL111':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL111,
			'SEL011':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL011,
			'SEL010':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL010,
			'SEL000':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL000,
			'SEL001':_b.KXG08_FSYNC_CTL_FSYNC_SEL_SEL001,
		}
		self.KXG08_AUX_I2C_ODR2_AUX2ODR={
			'25':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_25,
			'0P781':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_0P781,
			'200':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_200,
			'12P5':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_12P5,
			'1600':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1600,
			'50':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_50,
			'1600_3':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_3,
			'1P563':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1P563,
			'3P125':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_3P125,
			'400':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_400,
			'100':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_100,
			'1600_4':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_4,
			'800':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_800,
			'1600_2':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_2,
			'6P25':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_6P25,
			'1600_1':_b.KXG08_AUX_I2C_ODR2_AUX2ODR_1600_1,
		}
		self.KXG08_FSYNC_CTL_FSYNC_TRIG={
			'FSYNC':_b.KXG08_FSYNC_CTL_FSYNC_TRIG_FSYNC,
			'INT2':_b.KXG08_FSYNC_CTL_FSYNC_TRIG_INT2,
		}
		self.KXG08_ACCEL_CTL_ACC_BW={
			'ODR_8':_b.KXG08_ACCEL_CTL_ACC_BW_ODR_8,
			'ODR_2':_b.KXG08_ACCEL_CTL_ACC_BW_ODR_2,
		}
		self.KXG08_TILT_TAP_ODR_OTP={
			'50_2':_b.KXG08_TILT_TAP_ODR_OTP_50_2,
			'25':_b.KXG08_TILT_TAP_ODR_OTP_25,
			'50_1':_b.KXG08_TILT_TAP_ODR_OTP_50_1,
			'12P5':_b.KXG08_TILT_TAP_ODR_OTP_12P5,
			'50':_b.KXG08_TILT_TAP_ODR_OTP_50,
			'1P563':_b.KXG08_TILT_TAP_ODR_OTP_1P563,
			'3P125':_b.KXG08_TILT_TAP_ODR_OTP_3P125,
			'6P25':_b.KXG08_TILT_TAP_ODR_OTP_6P25,
		}
		self.KXG08_STDBY_GYRO_STDBY={
			'DISABLED':_b.KXG08_STDBY_GYRO_STDBY_DISABLED,
			'ENABLED':_b.KXG08_STDBY_GYRO_STDBY_ENABLED,
		}
		self.KXG08_INT2_SRC4_INT2_TDTS={
			'SINGLE_TAP':_b.KXG08_INT2_SRC4_INT2_TDTS_SINGLE_TAP,
			'NO_TAP_EVENT':_b.KXG08_INT2_SRC4_INT2_TDTS_NO_TAP_EVENT,
			'DOUBLE_TAP':_b.KXG08_INT2_SRC4_INT2_TDTS_DOUBLE_TAP,
		}
		self.KXG08_STDBY_TEMP_STDBY={
			'DISABLED':_b.KXG08_STDBY_TEMP_STDBY_DISABLED,
			'ENABLED':_b.KXG08_STDBY_TEMP_STDBY_ENABLED,
		}
		self.KXG08_AUX_STATUS_AUX2ST={
			'DISABLED':_b.KXG08_AUX_STATUS_AUX2ST_DISABLED,
			'SENSOR_RUNNING':_b.KXG08_AUX_STATUS_AUX2ST_SENSOR_RUNNING,
			'WAITING_TO_BE_DISABLED':_b.KXG08_AUX_STATUS_AUX2ST_WAITING_TO_BE_DISABLED,
			'WAITING_TO_BE_ENABLED':_b.KXG08_AUX_STATUS_AUX2ST_WAITING_TO_BE_ENABLED,
		}
		self.KXG08_GYRO_ODR_NAVGG={
			'4_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_4_SAMPLE_AVG,
			'16_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_16_SAMPLE_AVG,
			'8_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_8_SAMPLE_AVG,
			'NO_AVG':_b.KXG08_GYRO_ODR_NAVGG_NO_AVG,
			'128_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_128_SAMPLE_AVG,
			'2_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_2_SAMPLE_AVG,
			'64_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_64_SAMPLE_AVG,
			'32_SAMPLE_AVG':_b.KXG08_GYRO_ODR_NAVGG_32_SAMPLE_AVG,
		}
		self.KXG08_ACCEL_CTL_ACC_FS={
			'4G':_b.KXG08_ACCEL_CTL_ACC_FS_4G,
			'2G':_b.KXG08_ACCEL_CTL_ACC_FS_2G,
			'8G':_b.KXG08_ACCEL_CTL_ACC_FS_8G,
			'16G':_b.KXG08_ACCEL_CTL_ACC_FS_16G,
		}
		self.KXG08_INT1_SRC4_INT1_TDTS={
			'DOUBLE':_b.KXG08_INT1_SRC4_INT1_TDTS_DOUBLE,
			'SINGLE':_b.KXG08_INT1_SRC4_INT1_TDTS_SINGLE,
			'NOTAP':_b.KXG08_INT1_SRC4_INT1_TDTS_NOTAP,
		}
		self.KXG08_WAKE_SLEEP_CTL1_C_MODE={
			'COUNTER_DECREMENT':_b.KXG08_WAKE_SLEEP_CTL1_C_MODE_COUNTER_DECREMENT,
			'COUNTER_CLEAR':_b.KXG08_WAKE_SLEEP_CTL1_C_MODE_COUNTER_CLEAR,
		}
		self.KXG08_STDBY_AUX1_STDBY={
			'DISABLED':_b.KXG08_STDBY_AUX1_STDBY_DISABLED,
			'ENABLED':_b.KXG08_STDBY_AUX1_STDBY_ENABLED,
		}
		self.KXG08_AUX_STATUS_AUX1ST={
			'DISABLED':_b.KXG08_AUX_STATUS_AUX1ST_DISABLED,
			'SENSOR_RUNNING':_b.KXG08_AUX_STATUS_AUX1ST_SENSOR_RUNNING,
			'WAITING_TO_BE_DISABLED':_b.KXG08_AUX_STATUS_AUX1ST_WAITING_TO_BE_DISABLED,
			'WAITING_TO_BE_ENABLED':_b.KXG08_AUX_STATUS_AUX1ST_WAITING_TO_BE_ENABLED,
		}
		self.KXG08_FFCTL_DCRM={
			'UP_RESET':_b.KXG08_FFCTL_DCRM_UP_RESET,
			'UP_DOWN':_b.KXG08_FFCTL_DCRM_UP_DOWN,
		}
		self.KXG08_INT_PIN_CTL_IEA1={
			'ACTIVE_HIGH':_b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_HIGH,
			'ACTIVE_LOW':_b.KXG08_INT_PIN_CTL_IEA1_ACTIVE_LOW,
		}
		self.KXG08_INT_PIN_CTL_IEA2={
			'ACTIVE_HIGH':_b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_HIGH,
			'ACTIVE_LOW':_b.KXG08_INT_PIN_CTL_IEA2_ACTIVE_LOW,
		}
		self.KXG08_GYRO_CTL_GYRO_FS={
			'1024':_b.KXG08_GYRO_CTL_GYRO_FS_1024,
			'TBD2':_b.KXG08_GYRO_CTL_GYRO_FS_TBD2,
			'2048':_b.KXG08_GYRO_CTL_GYRO_FS_2048,
			'TBD1':_b.KXG08_GYRO_CTL_GYRO_FS_TBD1,
			'64':_b.KXG08_GYRO_CTL_GYRO_FS_64,
			'128':_b.KXG08_GYRO_CTL_GYRO_FS_128,
			'512':_b.KXG08_GYRO_CTL_GYRO_FS_512,
			'256':_b.KXG08_GYRO_CTL_GYRO_FS_256,
		}
		self.KXG08_TILT_TAP_ODR_OTDT={
			'25':_b.KXG08_TILT_TAP_ODR_OTDT_25,
			'200':_b.KXG08_TILT_TAP_ODR_OTDT_200,
			'12P5':_b.KXG08_TILT_TAP_ODR_OTDT_12P5,
			'1600':_b.KXG08_TILT_TAP_ODR_OTDT_1600,
			'50':_b.KXG08_TILT_TAP_ODR_OTDT_50,
			'400':_b.KXG08_TILT_TAP_ODR_OTDT_400,
			'100':_b.KXG08_TILT_TAP_ODR_OTDT_100,
			'800':_b.KXG08_TILT_TAP_ODR_OTDT_800,
		}
		self.KXG08_FSYNC_CTL_FSYNC_MODE={
			'DISABLED':_b.KXG08_FSYNC_CTL_FSYNC_MODE_DISABLED,
			'INPUT_EXT':_b.KXG08_FSYNC_CTL_FSYNC_MODE_INPUT_EXT,
			'INPUT':_b.KXG08_FSYNC_CTL_FSYNC_MODE_INPUT,
			'OUTPUT':_b.KXG08_FSYNC_CTL_FSYNC_MODE_OUTPUT,
		}
		self.KXG08_STATUS2_WAKE_SLEEP={
			'SLEEP_MODE':_b.KXG08_STATUS2_WAKE_SLEEP_SLEEP_MODE,
			'WAKE_MODE':_b.KXG08_STATUS2_WAKE_SLEEP_WAKE_MODE,
		}
		self.KXG08_GYRO_CTL_GYRO_BW={
			'ODR_8':_b.KXG08_GYRO_CTL_GYRO_BW_ODR_8,
			'ODR_2':_b.KXG08_GYRO_CTL_GYRO_BW_ODR_2,
		}
		self.KXG08_WAKE_SLEEP_CTL1_TH_MODE={
			'ABSOLUTE_THRESHOLD':_b.KXG08_WAKE_SLEEP_CTL1_TH_MODE_ABSOLUTE_THRESHOLD,
			'RELATIVE_THRESHOLD':_b.KXG08_WAKE_SLEEP_CTL1_TH_MODE_RELATIVE_THRESHOLD,
		}
		self.KXG08_AUX_I2C_ODR_AUX1_D={
			'DNE':_b.KXG08_AUX_I2C_ODR_AUX1_D_DNE,
			'1':_b.KXG08_AUX_I2C_ODR_AUX1_D_1,
			'0':_b.KXG08_AUX_I2C_ODR_AUX1_D_0,
			'3':_b.KXG08_AUX_I2C_ODR_AUX1_D_3,
			'2':_b.KXG08_AUX_I2C_ODR_AUX1_D_2,
			'5':_b.KXG08_AUX_I2C_ODR_AUX1_D_5,
			'4':_b.KXG08_AUX_I2C_ODR_AUX1_D_4,
			'6':_b.KXG08_AUX_I2C_ODR_AUX1_D_6,
		}
		self.KXG08_WAKE_SLEEP_CTL1_OWUF={
			'25':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_25,
			'0P781':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_0P781,
			'12P5':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_12P5,
			'50':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_50,
			'1P563':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_1P563,
			'3P125':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_3P125,
			'100':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_100,
			'6P25':_b.KXG08_WAKE_SLEEP_CTL1_OWUF_6P25,
		}
		self.KXG08_STATUS1_WAKE_SLEEP={
			'SLEEP_MODE':_b.KXG08_STATUS1_WAKE_SLEEP_SLEEP_MODE,
			'WAKE_MODE':_b.KXG08_STATUS1_WAKE_SLEEP_WAKE_MODE,
		}
		self.KXG08_AUX_I2C_ODR2_AUX2_D={
			'DNE':_b.KXG08_AUX_I2C_ODR2_AUX2_D_DNE,
			'1':_b.KXG08_AUX_I2C_ODR2_AUX2_D_1,
			'0':_b.KXG08_AUX_I2C_ODR2_AUX2_D_0,
			'3':_b.KXG08_AUX_I2C_ODR2_AUX2_D_3,
			'2':_b.KXG08_AUX_I2C_ODR2_AUX2_D_2,
			'5':_b.KXG08_AUX_I2C_ODR2_AUX2_D_5,
			'4':_b.KXG08_AUX_I2C_ODR2_AUX2_D_4,
			'6':_b.KXG08_AUX_I2C_ODR2_AUX2_D_6,
		}
		self.KXG08_AUX_I2C_ODR_AUX1ODR={
			'25':_b.KXG08_AUX_I2C_ODR_AUX1ODR_25,
			'0P781':_b.KXG08_AUX_I2C_ODR_AUX1ODR_0P781,
			'200':_b.KXG08_AUX_I2C_ODR_AUX1ODR_200,
			'12P5':_b.KXG08_AUX_I2C_ODR_AUX1ODR_12P5,
			'1600':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1600,
			'50':_b.KXG08_AUX_I2C_ODR_AUX1ODR_50,
			'1600_3':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1600_3,
			'1P563':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1P563,
			'3P125':_b.KXG08_AUX_I2C_ODR_AUX1ODR_3P125,
			'400':_b.KXG08_AUX_I2C_ODR_AUX1ODR_400,
			'100':_b.KXG08_AUX_I2C_ODR_AUX1ODR_100,
			'1600_4':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1600_4,
			'800':_b.KXG08_AUX_I2C_ODR_AUX1ODR_800,
			'1600_2':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1600_2,
			'6P25':_b.KXG08_AUX_I2C_ODR_AUX1ODR_6P25,
			'1600_1':_b.KXG08_AUX_I2C_ODR_AUX1ODR_1600_1,
		}
		self.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP={
			'DISABLED':_b.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP_DISABLED,
			'ENABLED':_b.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP_ENABLED,
		}
		self.KXG08_ACCEL_ODR_NAVGA={
			'4_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_4_SAMPLE_AVG,
			'16_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_16_SAMPLE_AVG,
			'8_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_8_SAMPLE_AVG,
			'NO_AVG':_b.KXG08_ACCEL_ODR_NAVGA_NO_AVG,
			'128_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_128_SAMPLE_AVG,
			'2_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_2_SAMPLE_AVG,
			'64_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_64_SAMPLE_AVG,
			'32_SAMPLE_AVG':_b.KXG08_ACCEL_ODR_NAVGA_32_SAMPLE_AVG,
		}
		self.KXG08_INT_PIN_CTL_IEL2={
			'PULSED_50US':_b.KXG08_INT_PIN_CTL_IEL2_PULSED_50US,
			'PULSED_200US':_b.KXG08_INT_PIN_CTL_IEL2_PULSED_200US,
			'LATCHED':_b.KXG08_INT_PIN_CTL_IEL2_LATCHED,
			'REALTIME':_b.KXG08_INT_PIN_CTL_IEL2_REALTIME,
		}
		self.KXG08_INT_PIN_CTL_IEL1={
			'PULSED_50US':_b.KXG08_INT_PIN_CTL_IEL1_PULSED_50US,
			'PULSED_200US':_b.KXG08_INT_PIN_CTL_IEL1_PULSED_200US,
			'LATCHED':_b.KXG08_INT_PIN_CTL_IEL1_LATCHED,
			'REALTIME':_b.KXG08_INT_PIN_CTL_IEL1_REALTIME,
		}
		self.KXG08_STDBY_AUX2_STDBY={
			'DISABLED':_b.KXG08_STDBY_AUX2_STDBY_DISABLED,
			'ENABLED':_b.KXG08_STDBY_AUX2_STDBY_ENABLED,
		}
class masks(register_base):
	def __init__(self):
		self.KXG08_BUF_SMPLEV_L_SMP_LEV3_0_MASK                   = 0xF0         # Reports the number of data packets (ODR cycles) currently stored in the buffer.
		self.KXG08_BUF_SMPLEV_H_SMP_LEV11_4_MASK                  = 0xFF         
		self.KXG08_AUX_STATUS_AUX1ST_MASK                         = 0x03         # Detailed aux1 communication status.
		self.KXG08_AUX_STATUS_AUX2ST_MASK                         = 0x30         # Detailed aux1 communication status.
		self.KXG08_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KXG08_STATUS1_WAKE_SLEEP_MASK                        = 0x04         # Wake/sleep status flag
		self.KXG08_INT1_SRC4_INT1_TDTS_MASK                       = 0x06         # Tap/DoubleTap interrupt source.
		self.KXG08_STATUS2_WAKE_SLEEP_MASK                        = 0x04         # Wake/sleep status flag
		self.KXG08_INT2_SRC4_INT2_TDTS_MASK                       = 0x06         
		self.KXG08_ACCEL_ODR_NAVGA_MASK                           = 0x70         # Accelerometer OSR control.
		self.KXG08_ACCEL_ODR_ODRA_MASK                            = 0x0F         
		self.KXG08_ACCEL_CTL_ACC_BW_MASK                          = 0x08         # Accelerometer bandwidth control.
		self.KXG08_ACCEL_CTL_ACC_FS_MASK                          = 0x03         # Accelerometer full scale range select.
		self.KXG08_GYRO_ODR_NAVGG_MASK                            = 0x70         
		self.KXG08_GYRO_ODR_ODRG_MASK                             = 0x0F         
		self.KXG08_GYRO_CTL_GYRO_BW_MASK                          = 0x08         
		self.KXG08_GYRO_CTL_GYRO_FS_MASK                          = 0x07         
		self.KXG08_INT_PIN_CTL_IEA2_MASK                          = 0x40         # Interrupt polarity select for INT2 pin.
		self.KXG08_INT_PIN_CTL_IEL2_MASK                          = 0x30         # Interrupt latch mode select for INT2 pin
		self.KXG08_INT_PIN_CTL_IEA1_MASK                          = 0x04         # Interrupt polarity select for INT1 pin.
		self.KXG08_INT_PIN_CTL_IEL1_MASK                          = 0x03         # Interrupt latch mode select for INT1 pin
		self.KXG08_FSYNC_CTL_FSYNC_TRIG_MASK                      = 0x40         # Defines INT2 and SYNC_TRIG pin functionality
		self.KXG08_FSYNC_CTL_FSYNC_MODE_MASK                      = 0x30         # FSYNC enable and mode select.
		self.KXG08_FSYNC_CTL_FSYNC_SEL_MASK                       = 0x07         
		self.KXG08_WAKE_SLEEP_CTL1_TH_MODE_MASK                   = 0x20         
		self.KXG08_WAKE_SLEEP_CTL1_C_MODE_MASK                    = 0x10         # Defines de-bounce counter clear mode.
		self.KXG08_WAKE_SLEEP_CTL1_OWUF_MASK                      = 0x07         # sets the Output Data Rate for the Wake-up (motion detection).
		self.KXG08_WAKE_SLEEP_CTL2_OBTS_MASK                      = 0x0F         # sets the Output Data Rate for the Back to Sleep (BTS).
		self.KXG08_AUX_I2C_CTL_REG_AUX_BUS_SPD_MASK               = 0x08         # Sets I2C bus speed.
		self.KXG08_AUX_I2C_CTL_REG_AUX_PULL_UP_MASK               = 0x04         # Active pullup
		self.KXG08_AUX_I2C_ODR_AUX1_D_MASK                        = 0x70         # Number of bytes read back via Auxiliary I2C bus from device
		self.KXG08_AUX_I2C_ODR_AUX1ODR_MASK                       = 0x0F         # Determines rate at which aux1 output is polled by ASIC in aux
		self.KXG08_AUX_I2C_ODR2_AUX2_D_MASK                       = 0x70         # Number of bytes read back via Auxiliary I2C bus from device
		self.KXG08_AUX_I2C_ODR2_AUX2ODR_MASK                      = 0x0F         # Determines rate at which aux1 output is polled by ASIC in aux
		self.KXG08_TILT_TAP_ODR_OTDT_MASK                         = 0x38         
		self.KXG08_TILT_TAP_ODR_OTP_MASK                          = 0x07         
		self.KXG08_FFCTL_ULMODE_MASK                              = 0x40         # Free fall interrupt latch/un-latch control
		self.KXG08_FFCTL_DCRM_MASK                                = 0x08         # Debounce methodology control
		self.KXG08_FFCTL_OFFI_MASK                                = 0x07         
		self.KXG08_STDBY_TEMP_STDBY_MASK                          = 0x20         # Active low Temperature sensor enable.
		self.KXG08_STDBY_AUX2_STDBY_MASK                          = 0x10         # Active low aux2 sensor enable.
		self.KXG08_STDBY_AUX1_STDBY_MASK                          = 0x08         # Active low aux1 sensor enable.
		self.KXG08_STDBY_GYRO_FSTART_MASK                         = 0x04         # Active high gyroscope fast start sensor enable
		self.KXG08_STDBY_GYRO_STDBY_MASK                          = 0x02         # Active low gyroscope sensor enable.
		self.KXG08_STDBY_ACC_STDBY_MASK                           = 0x01         # Active low Accelerometer sensor enable.
		self.KXG08_BUF_WMITH_L_SMP_TH13_0_MASK                    = 0xF0         # Read/write control register that controls the buffer sample threshold.
		self.KXG08_BUF_WMITH_H_SMP_TH11_4_MASK                    = 0xFF         # Read/write control register that controls the buffer sample threshold.
		self.KXG08_BUF_TRIGTH_L_TRIG_TH3_0_MASK                   = 0xF0         # Buffer Trigger mode threshold L
		self.KXG08_BUF_TRIGTH_H_TRIG_TH11_4_MASK                  = 0xFF         # Buffer Trigger mode threshold H
		self.KXG08_BUF_EN_BUF_M_MASK                              = 0x03         # selects the operating mode of the sample buffer
		self.KXG08_2080_WHO_AM_I_WIA_MASK                         = 0xFF         
		self.KXG07_1080_WHO_AM_I_WIA_MASK                         = 0xFF         
		self.KXG07_2080_WHO_AM_I_WIA_MASK                         = 0xFF         
		self.KXG07_3001_WHO_AM_I_WIA_MASK                         = 0xFF         