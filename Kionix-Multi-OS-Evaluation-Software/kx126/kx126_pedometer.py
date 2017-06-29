# The MIT License (MIT)
#
# Copyright (c) 2016 Kionix Inc.
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
## Example application for basic pedometer step counting
###
## Pedometer uses interrupts int1 for step event and int2 for watermark event
###
 
import time
from imports import *
from lib.data_stream import stream_config, timenow_str, start_time_str, end_time_str
from lib.proto import ProtocolException

class kx126_pedometer_data_stream(stream_config):
    def __init__(self, sensor):
        stream_config.__init__(self)

        # define the data stream
        ped_gpio_pin  = 1 # index number
        self.define_request_message(sensor,
                                    fmt = "<BBBBBBB",
                                    hdr = "ch!ins1!ins2!ins3!stat!N/A!rel",
                                    reg = r.KX126_INS1,
                                    pin_index=ped_gpio_pin)

# TODO : remove methods below when proto.py is updated
    def _start_streaming(self, sensor):
        # send stream start requests to FW
        for request in self.request_message_list:
            resp=sensor._bus.enable_interrupt(*request.msg_req)
            self.msg_ind_dict[resp] = request

    def _receive_data(self, sensor):
        # wait for steps forever
        while 1:
            resp = sensor._bus.wait_indication()
            if resp is not None:
                break

        # find correct message type to get information how message is interpreted
        # resp[0] has the channel number
        received_messsage_type = self.msg_ind_dict[resp[0]]

        if len(resp) !=received_messsage_type.msg_size:
            assert 0,"Wrong message length %d" % len(resp)
        else:
            data = struct.unpack(received_messsage_type.msg_fmt, resp)

        return data

    def _stop_streaming(self, sensor):
        sensor._bus._flush_input()        

        # send stream stop requests to FW in reversed order
        for request in reversed(self.request_message_list):
            sensor._bus.disable_interrupt(request.gpio_pin)
        
    def read_data_stream(self, sensor, loop, callback = None):
        self._start_streaming(sensor)
        DELIMITER = ';\t'
        count = 0
        print start_time_str()
        print '\n'
        
        try:
            while count < loop or loop is None:
                try:
                    now = timing.time_elapsed()
                    data = self._receive_data(sensor)

                    text = DELIMITER.join('{:d}'.format(t) for t in data)
                    print '%f%s%s' % (now, DELIMITER, text)
                    count += 1

                except ProtocolException,e:
                    # expecting that it is just timeout
                    # print 'timeout',e
                    pass

        except KeyboardInterrupt:
            print '\n'
            print end_time_str()
            print '\n'
            print 'Steps counted:', sensor.read_step_count()
            pass

        finally:
            self._stop_streaming(sensor)
            pass

## Pedometer outputs
##
## ins1, STPOVI = step overflow event
## ins1, STPWMI = step watermark event
## ins2, STPINCI = step counter increment event

## Enabler methods for the asic features
##
## set pedometer parameters
def set_pedometer_parameters_odr_100(sensor):
    ##### pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.

    ## PED_CNTL1
    ##      STP_TH; first accepted step count level = default 8 (0x4)
    ##      MAG_SCALE; signal scaling = default 6
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, b.KX126_PED_CNTL1_STP_TH_STEP_12, m.KX126_PED_CNTL1_STP_TH_MASK) # 12 steps
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, 0x06 << 0, m.KX126_PED_CNTL1_MAG_SCALE_MASK)

    ## PED_CNTL2
    ##      HPS; Scaling factor for the output from the high-pass filter = default 3
    ##      LP_LEN; The length of the low-pass filter = default 100Hz (0x0c)
    ## default 03 changed due 8g mode in asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, 0x02 << 4, m.KX126_PED_CNTL2_HPS_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_100, m.KX126_PED_CNTL2_PED_ODR_MASK)
        
    ## PED_CNTL3
    ##      FCB; Scaling factors inside the high-pass filter = default 0x01, changed due to the 8g mode in the asic
    ##      FCA; Default 0x0E, changed due to the 8g mode in the asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, 0x02 << 3, m.KX126_PED_CNTL3_FCB_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, 0x07 << 0, m.KX126_PED_CNTL3_FCA_MASK)
 
    ## PED_CNTL4
    ##      B_CNT; Samples below the zero threshold before setting = default 0x1
    ##      A_H; Maximum area of the peak (maximum impact from the floor) = default 0x0F
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, 0x01 << 4, m.KX126_PED_CNTL4_B_CNT_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, 0x0F << 0, m.KX126_PED_CNTL4_A_H_MASK)
    
    ## PED_CNTL5
    ##      A_L; Minimum area of the peak (minimum impact from the floor) = default 0x3C
    sensor.write_register(r.KX126_PED_CNTL5, 0x24)
            
    ## PED_CNTL6
    ##      M_H; maximum time interval for the peak = default 0x14
    sensor.write_register(r.KX126_PED_CNTL6, 0x13)
    
    ## PED_CNTL7
    ##      M_L         - minimum time interval for the peak = default 0x06
    sensor.write_register(r.KX126_PED_CNTL7, 0x0B)
    
    ## PED_CNTL8
    ##      T_L         - time window for noise and delay time = default 0x05
    sensor.write_register(r.KX126_PED_CNTL8,0x08)
        
    ## PED_CNTL9
    ##      T_M         - time interval to prevent overflowing = default 0x16
    sensor.write_register(r.KX126_PED_CNTL9,0x19)
    
    ## PED_CNTL10
    ##      T_P         - minimum time interval for a single stride = default 0x13
    sensor.write_register(r.KX126_PED_CNTL10,0x1C)

def set_pedometer_parameters_odr_50(sensor):
    ##### pedometer algorithm settings, configuration ODR_50, ODR = 50 Hz.

    ## PED_CNTL1
    ##      STP_TH; first accepted step count level = default 8 (0x4)
    ##      MAG_SCALE; signal scaling = default 6
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, b.KX126_PED_CNTL1_STP_TH_STEP_8, m.KX126_PED_CNTL1_STP_TH_MASK) # 8 steps
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, 0x06 << 0, m.KX126_PED_CNTL1_MAG_SCALE_MASK)

    ## PED_CNTL2
    ##      HPS; Scaling factor for the output from the high-pass filter = default 3
    ##      LP_LEN; The length of the low-pass filter = default 100Hz (0x0c)
    ## default 03 changed due 8g mode in asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, 0x02 << 4, m.KX126_PED_CNTL2_HPS_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_50, m.KX126_PED_CNTL2_PED_ODR_MASK) # ODR = 50 Hz
        
    ## PED_CNTL3
    ##      FCB; Scaling factors inside the high-pass filter = default 0x01, changed due to the 8g mode in the asic
    ##      FCA; Default 0x0E, changed due to the 8g mode in the asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, 0x02 << 3, m.KX126_PED_CNTL3_FCB_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, 0x07 << 0, m.KX126_PED_CNTL3_FCA_MASK)
 
    ## PED_CNTL4
    ##      B_CNT; Samples below the zero threshold before setting = default 0x1
    ##      A_H; Maximum area of the peak (maximum impact from the floor) = default 0x0F
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, 0x01 << 4, m.KX126_PED_CNTL4_B_CNT_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, 0x0F << 0, m.KX126_PED_CNTL4_A_H_MASK)
    
    ## PED_CNTL5
    ##      A_L; Minimum area of the peak (minimum impact from the floor) = default 0x3C
    sensor.write_register(r.KX126_PED_CNTL5, 0x10)
            
    ## PED_CNTL6
    ##      M_H; maximum time interval for the peak = default 0x14
    sensor.write_register(r.KX126_PED_CNTL6, 0x0A)
    
    ## PED_CNTL7
    ##      M_L         - minimum time interval for the peak = default 0x06
    sensor.write_register(r.KX126_PED_CNTL7, 0x0B)
    
    ## PED_CNTL8
    ##      T_L         - time window for noise and delay time = default 0x05
    sensor.write_register(r.KX126_PED_CNTL8,0x05)
        
    ## PED_CNTL9
    ##      T_M         - time interval to prevent overflowing = default 0x16
    sensor.write_register(r.KX126_PED_CNTL9,0x10)
    
    ## PED_CNTL10
    ##      T_P         - minimum time interval for a single stride = default 0x13
    sensor.write_register(r.KX126_PED_CNTL10,0x0A)

## enable measurement and pedometer logger
def kx126_enable_pedometer_logger(sensor, odr = 100, avg = 128):
    logger.info('Pedometer step counting init start')

    # turn sensor off
    sensor.set_power_off()         # this sensor request PC=0 to PC=1 before valid settings
  
    # set watermark interrupt level
    #sensor.set_pedometer_watermark(0x14)
    
    # "disable" watermark
    sensor.set_pedometer_watermark(0xffff)

    if odr == 50:
        # run pedometer with 50Hz ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_50, m.KX126_PED_CNTL2_PED_ODR_MASK)
    else: # run pedometer with 100Hz ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_100, m.KX126_PED_CNTL2_PED_ODR_MASK)
    
    if  avg == 0: # no averaging
        sensor.set_average(b.KX126_LP_CNTL_AVC_NO_AVG)
    elif avg == 2: # set averaging to 2 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_2_SAMPLE_AVG)
    elif avg == 4: # set averaging to 4 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_4_SAMPLE_AVG)
    elif avg == 8: # set averaging to 8 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_8_SAMPLE_AVG)
    elif avg == 16: # set averaging to 16 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_16_SAMPLE_AVG)
    elif avg == 32: # set averaging to 32 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_32_SAMPLE_AVG)
    elif avg == 64: # set averaging to 64 samples
        sensor.set_average(b.KX126_LP_CNTL_AVC_64_SAMPLE_AVG)
    elif avg == 128: # set averaging to 128 samples - high performance mode
        sensor.set_average(b.KX126_LP_CNTL_AVC_128_SAMPLE_AVG)
    else: sensor.set_average(b.KX126_LP_CNTL_AVC_128_SAMPLE_AVG) # Default number for averaging

    # configure interrupts  
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPOVI2) # overflow interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPWMI2) # watermark interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPINCI2) # step counter increment interrupt to INT2
    
    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2 ) # enable INT2
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEA2 ) # active low 
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2 ) # latched interrupt
    
    sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_PDE ) # enable pedometer
    
    logger.info('Pedometer step counting initialized')
    #sensor.set_power_on()                             # power on the sensor

def read_with_polling(sensor, loop):
    count = 0
   
    try:
        while count < loop or loop is None:
            ins1 = sensor.read_register(r.KX126_INS1)[0]
            ins2 = sensor.read_register(r.KX126_INS2)[0]
            now = timing.time_elapsed()
            
            # pedometer interrupts
            if ins1 & b.KX126_INS1_STPWMI:
                logger.info('KX126_INS1_STPWMI')
                print 'WMI steps',sensor.read_step_count()

            if ins2 & b.KX126_INS2_STPINCI:
                logger.info('KX126_INS2_STPINCI')
                print '%f%s%d%s%d%s%d' % (now,DELIMITER,10, DELIMITER, ins1, DELIMITER, ins2)

            if ins1 & b.KX126_INS1_STPOVI:
                logger.debug('KX126_INS1_STPOVI')

            # other interrupts
            if ins2 & b.KX126_INS2_WMI:
                logger.debug('KX126_INS2_WMI')

            if ins2 & b.KX126_INS2_BFI:
                logger.debug('KX126_INS2_BFI')

            if ins2 & b.KX126_INS2_FFS:
                logger.debug('KX126_INS2_FFS')

            if ins2 ^ b.KX126_INS2_DRDY != 0:
                #print '%f%s%d%s%d%s%d' % (now,DELIMITER,10, DELIMITER, ins1, DELIMITER, ins2)
                sensor.release_interrupts()
                count += 1
                    
    except(KeyboardInterrupt):
        print '\n'
        print 'Steps counted:', sensor.read_step_count()
        print '\n'
    
    finally:
        logger.info('bye')

def read_with_stream(sensor, loop=None):
    stream = kx126_pedometer_data_stream(sensor)
    stream.read_data_stream(sensor, loop)
    #sensor._bus._flush_input()
    #print('steps counted %d ' % sensor.read_step_count())
    return stream

def enable_data_logging(kx126_drv, odr = 100, mode = 2, avg = 128):
    
    kx126_enable_pedometer_logger(kx126_drv, odr, avg)

    if mode == 1: set_pedometer_parameters_odr_50(kx126_drv)
    elif mode == 2: set_pedometer_parameters_odr_100(kx126_drv)
    else : set_pedometer_parameters_odr_100(kx126_drv)

    print 'Enable_data_logging for', odr, 'Hz,', 'avg =', avg, ', mode =', mode
    kx126_drv.set_power_on()

if __name__ == '__main__':

    # A default ODR for the pedometer
    odr = 100
    # A default number of AVG samples for the pedometer engine
    avg = 128
    # Select configuration related to the ODR
    #conf = 1 # with ODR = 50 Hz
    conf = 2  # with ODR = 100 Hz
    
    bus = setup_default_connection()
    kx126_drv = kx126_driver()

    bus.probe_sensor(kx126_drv)

    if conf == 1: # The best configuration with 50 Hz ODR.
        odr = 50
        enable_data_logging(kx126_drv, odr, conf, avg)
    elif conf == 2:  # The best configuration with 100 Hz ODR.
        enable_data_logging(kx126_drv, odr, conf, avg)
    else: # A default configuration.
        enable_data_logging(kx126_drv, odr, conf, avg)

    logger.info('kx126_pedometer; '+'ODR: ' + str(odr)+' Hz, '+'configuration: '+str(conf)+', avg: '+str(avg)+' samples')
    
    timing.reset()

    if args.stream_mode:
        if stream_config_check() is True:
            logger.info('Read with stream')
            print '\n'
            read_with_stream(kx126_drv)
        else:
            logger.error(stream_config_check())
    else:
        logger.info('Read with polling')
        print "\n"
        read_with_polling(kx126_drv, args.loop)
   
    kx126_drv.set_power_off()
    bus.close()
    