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
"""
Example app for WakeUp/Back To Sleep  (WU and BTS) detection

WakeUp and Back sleep uses INT2 interrupt and DataReady INT1
both register and int pin polling could be used
For KX126 wakeup detection works always with +-8g range
"""

_CODE_FORMAT_VERSION = 2.0
from imports import *

## wake and sleep status
wakesleep_status = {
    0: 'Sleep',
    1: 'Wake'}

####
## threshold and counter values for wuf and bts
#### example wakeup/back to sleep values (fast transitions)
## values for 2g and 12.5Hz odr for both OWUF and OBTS
## OSA (stream odr) = 25Hz (> OWUF & OBTS)
class Parameter_set_1:

    WUF_THRESHOLD_VALUE = 260           # 3.9mg*value
    WUF_COUNTER_VALUE   = 2             # 1/OWUF*value
    BTS_THRESHOLD_VALUE = 200           # 3.9mg*value
    BTS_COUNTER_VALUE   = 40            # 1/OBTS*value
    LOW_POWER_MODE      = False
    lp_average          = '16_SAMPLE_AVG'
    odr_OSA             = 25
    odr_OWUF            = 12.5
    odr_OBTS            = 12.5
    
## wuf/bts direction axes masks
WUF_AXES        =   b.KX126_INC2_XNWUE | \
                    b.KX126_INC2_XPWUE | \
                    b.KX126_INC2_YNWUE | \
                    b.KX126_INC2_YPWUE | \
                    b.KX126_INC2_ZNWUE | \
                    b.KX126_INC2_ZPWUE

## wuf directions source
wufbts_direction = {
                    b.KX126_INS3_ZNWU : "FACE_UP",
                    b.KX126_INS3_ZPWU : "FACE_DOWN",
                    b.KX126_INS3_XNWU : "UP",
                    b.KX126_INS3_XPWU : "DOWN",
                    b.KX126_INS3_YPWU : "RIGHT",
                    b.KX126_INS3_YNWU : "LEFT" }

SLEEP, WAKE = range(2)


def wake_sleep(sensor, mode):                                   # select wake or sleep mode manually
    assert mode in [SLEEP, WAKE]
    if mode == WAKE:
        sensor.set_bit(r.KX126_CNTL5, b.KX126_CNTL5_MAN_WAKE)           # wait until wake setup bit released 
        while sensor.read_register(r.KX126_CNTL5, 1)[0] & \
                                   b.KX126_CNTL5_MAN_WAKE <> 0: pass    # wait until wake mode valid
        while sensor.read_register(r.KX126_STAT, 1)[0] & b.KX126_STAT_WAKE == 0: pass
        return
    elif mode == SLEEP:
        sensor.set_bit(r.KX126_CNTL5, b.KX126_CNTL5_MAN_SLEEP)          # wait until sleep setup bit released
        while sensor.read_register(r.KX126_CNTL5, 1)[0] & \
                                   b.KX126_CNTL5_MAN_SLEEP <> 0: pass   # wait until sleep mode valid
        while sensor.read_register(r.KX126_STAT, 1)[0] & b.KX126_STAT_WAKE > 0: pass
        return

def directions(dir):            # print wuf+bts source directions
    fst = True
    pos = None
    for i in range(0, 6):
        mask = 0x01 << i
        if dir & mask > 0:
            if not fst:
                pos = pos + "+" + wufbts_direction[dir & mask]
            else:
                pos = wufbts_direction[dir & mask]
                fst = False
    return pos

def enable_wu_bts(  sensor,
                    cfg = Parameter_set_1,
                    power_off_on = True):
                    
    logger.info('Wakeup event init start')     
   
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
    'Invalid odr_OSA value "{}". Valid values are {}'.format(
    cfg.odr_OSA, e.KX126_ODCNTL_OSA.keys())
    
    assert convert_to_enumkey(cfg.odr_OWUF) in e.KX126_CNTL3_OWUF.keys(), \
    'Invalid odr_OWUF value "{}". Valid values are {}'.format(
    cfg.odr_OWUF,e.KX126_CNTL3_OWUF.keys())
    
    assert convert_to_enumkey(cfg.odr_OBTS) in e.KX126_CNTL4_OBTS.keys(), \
    'Invalid odr_OBTS value "{}". Valid values are {}'.format(
    cfg.odr_OBTS,e.KX126_CNTL4_OBTS.keys())
    
    assert cfg.LOW_POWER_MODE in [True,False],\
    'Invalid cfg.LOW_POWER_MODE value "{}". Valid values are {}'.format(
    cfg.LOW_POWER_MODE,[True, False])
    
    assert cfg.lp_average in e.KX126_LP_CNTL_AVC.keys(), \
    'Invalid lp_average value "{}". Valid values are {}'.format(
    cfg.lp_average, e.KX126_LP_CNTL_AVC.keys())

                    
    
    #Set sensor to stand-by to enable setup change

    if power_off_on:
        sensor.set_power_off()
    ##stream odr (if stream odr is biggest odr, it makes effect to current consumption)

    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])
    
    # g-range is fixed +-8g

    ## power modes
    if cfg.LOW_POWER_MODE:
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                          # low current
        ## set averaging (only for low power)
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])
    else:
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)         
  
    ## interrupt signal parameters
    sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEL1)  # latched interrupt
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2)  # latched interrupt
    assert evkit_config.get('generic','int1_active_high') in ['TRUE','FALSE']
    if evkit_config.get('generic','int1_active_high') == 'TRUE':
        sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEA1) # active high
    else:
        sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEA1)# active low
    if evkit_config.get('generic','int2_active_high') == 'TRUE':
        sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEA2)     # active high
    else:
        sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEA2)   # active low
        
    ## interrupt routings
    if evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy(intpin = 1)
        sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEN1)     # interrupt 1 set        
    elif evkit_config.get('generic','drdy_operation') == 'ADAPTER_GPIO2_INT':
        assert 0, "DataReady only to INT1, poll or timer"
    elif  evkit_config.get('generic','drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy(intpin = 1)        

    ## wakeup direction mask and occurence
    sensor.write_register(r.KX126_INC2, WUF_AXES)
    #sensor.set_bit(r.KX126_INC2, b.KX126_INC2_AOI_AND)
    sensor.reset_bit(r.KX126_INC2, b.KX126_INC2_AOI_OR)
    
    ## interrupt pin routings and settings for wu and bts
    sensor.set_bit(r.KX126_INC6, b.KX126_INC6_WUFI2)            # wu to int 2
    sensor.set_bit(r.KX126_INC6, b.KX126_INC6_BTSI2)            # bts to int 2
    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)             # enable int2 pin 

    ## function parameters
    ## wakeup and bts settings
    sensor.write_register(r.KX126_WUFTH, cfg.WUF_THRESHOLD_VALUE & 0x0ff)
    sensor.write_register(r.KX126_BTSTH, cfg.BTS_THRESHOLD_VALUE & 0x0ff)    
    msbs =((cfg.BTS_THRESHOLD_VALUE & 0x700) >> 4) | ((cfg.WUF_THRESHOLD_VALUE & 0x700) >> 8)
    sensor.write_register(r.KX126_BTSWUFTH, msbs)
    sensor.write_register(r.KX126_WUFC, cfg.WUF_COUNTER_VALUE & 0x0ff)
    sensor.write_register(r.KX126_BTSC, cfg.BTS_COUNTER_VALUE & 0x0ff)
 
    #sensor.set_bit(r.KX126_CTL4, b.KX126_CTL4_TH_MODE) # relative threshold (jerk)
    #sensor.set_bit(r.KX126_CTL4, b.KX126_CTL4_C_MODE)   # debounce counter method (decreased)

    sensor.set_bit(r.KX126_CNTL4, b.KX126_CNTL4_WUFE)                     # enable wuf
    sensor.set_bit(r.KX126_CNTL4, b.KX126_CNTL4_BTSE)                     # enable bts

    sensor.set_bit_pattern(r.KX126_CNTL3, e.KX126_CNTL3_OWUF[convert_to_enumkey(cfg.odr_OWUF)],  m.KX126_CNTL3_OWUF_MASK)
    sensor.set_bit_pattern(r.KX126_CNTL4, e.KX126_CNTL4_OBTS[convert_to_enumkey(cfg.odr_OBTS)],      m.KX126_CNTL4_OBTS_MASK)
    ## change mode (manual)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)
    
    # Turn on operating mode (disables setup) 
    ## power sensor(s)
    if power_off_on:
        sensor.set_power_on(CH_ACC )                                    # acc ON

    # sensor.register_dump()#sys.exit()

    sensor.release_interrupts()                                     # clear int
    sensor.read_data()                                              # this latches data ready interrupt register and signal
    logger.debug('enable_bts_wu done')

def readAndPrint(sensor, cur_bw_status, cur_count):
    sample_count = cur_count
    pin_condition = 0
    if evkit_config.get('generic','int1_active_high')=='TRUE':
        pin_condition = 1
        
    ## read wake/sleep status
    bw_status = wakesleep_status[sensor.read_register(r.KX126_STAT, 1)[0] & \
                                                      b.KX126_STAT_WAKE > 0]       
    if bw_status != cur_bw_status:              
        ## check interrupts
        if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':
            ## Read int pin (wu or bts)
            bw_event = sensor._bus.poll_gpio(2) == pin_condition
        else:
            ## Read from interrupt source register
            bw_ints = sensor.read_register(r.KX126_INS3, 1)[0]      # wu or bts
            bw_event = bw_ints & (b.KX126_INS3_WUFS | b.KX126_INS3_BTS) > 0
        
        ## direction position(s)
        pos = directions(sensor.read_register(r.KX126_INS3, 1)[0] & m.KX126_INS3_WU_MASK)    
            
        sensor.drdy_function()
        sample_count +=1
        data = sensor.read_data(CH_ACC)
        now_ms = int(time.clock() * 1000)
        
        print '%6d%s%5s%s%5d%s%6d%s%6d%s%6d' %( \
              now_ms,       DELIMITER,  \
              bw_status,    DELIMITER,  \
              sample_count, DELIMITER,  \
              data[0],      DELIMITER,  \
              data[1],      DELIMITER,  \
              data[2]),
        if pos == None:
            print ""
        else:
            print pos     # output data order; time, status, acc(xyz), (direction position)

        if bw_event:
            sensor.release_interrupts()
    else:
        sensor.drdy_function()
        data = sensor.read_data(CH_ACC)
        sample_count +=1        
    
    return bw_status, sample_count

def read_with_polling(sensor, loop):
    status = ""
    count = 0
    try:
        if loop == None:
            while 1:
                status, count = readAndPrint(sensor, status, count)
        else:
            for i in range(loop):
                status, count = readAndPrint(sensor, status, count)

    except(KeyboardInterrupt):
        pass 
def app_main():
    sensor = kx126_driver()
    bus = open_bus_or_exit(sensor)
    args = get_datalogger_args()   
    enable_wu_bts(sensor)
    read_with_polling(sensor, args.loop)
    
    logger.info("bye")
    sensor.set_power_off()    
    bus.close()

        
if __name__ == '__main__':
    app_main()
