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
 Example app for wakeup detection with fifo trigger
 after trigger and buffer full interrupts, data from fifo is stored to file in .\log directory

 Wakeup uses interrupt int2 and fifo full (BFI) interrupt int1
 interrupt int2 is internally transfered to fifo trigger

 NOTE : This test application does not work unless sensor's TRIG pad is physically connected to INT2 pad
"""
_CODE_FORMAT_VERSION = 2.0
from imports import *
from kx022_test_wu import enable_wakeup, Parameter_set_2, resultResolverToString,wu_bits_to_str
from kx022_data_logger import enable_data_logging


## select watermark level#
# samples (xyz), relates 8/16b resolution selection
watermark = 5
# samples, relates 8/16b resolution selection
buffer_size = [84, 42, 680, 340]

# buffer resolution is (1=8b or 2=16b)
BRES_8_BIT, BRES_16_BIT = [1,2]

def enable_wu_w_trig_fifo(sensor,
                          direction_mask=b.KX022_INC2_XNWUE |      # x- direction mask
                          b.KX022_INC2_XPWUE |      # x+ direction mask
                          b.KX022_INC2_YNWUE |      # y- direction mask
                          b.KX022_INC2_YPWUE |      # y+ direction mask
                          b.KX022_INC2_ZNWUE |      # z- direction mask
                          b.KX022_INC2_ZPWUE,      # z+ direction mask
                          cfg=Parameter_set_2,
                          bres=BRES_16_BIT,
                          ):

    logger.info('Wakeup event with FIFO -trigger started.')
    #
    # parameter validation
    #

    assert bres in [BRES_8_BIT, BRES_16_BIT], "wrong buffer resolution"

    # this sensor request PC=0 to PC=1 before valid settings
    sensor.set_power_off()

    #
    # Configure g-range, power mode and init wake up detection engine
    #
    enable_wakeup(sensor=sensor,
                  direction_mask=direction_mask,
                  cfg=cfg,
                  power_off_on=False)

    #
    # interrupt pin routings and settings
    #

    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin=1, polarity=ACTIVE_LOW)

    # enable buffer full to int1
    sensor.set_bit(r.KX022_INC4, b.KX022_INC4_BFI1)
    # latched interrupt for int1
    sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)
    # enable int1 pin
    sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEN1)

    #
    # fifo: mode and resolution
    #

    if bres == BRES_16_BIT:
        sensor.enable_fifo(mode=b.KX022_BUF_CNTL2_BUF_M_TRIGGER,
                           res=b.KX022_BUF_CNTL2_BRES)     # trigger and 16b
    else:
        # trigger and 8b
        sensor.enable_fifo(mode=b.KX022_BUF_CNTL2_BUF_M_TRIGGER, res=0)

    # enable buffer full function
    sensor.set_bit(r.KX022_BUF_CNTL2, b.KX022_BUF_CNTL2_BFIE)

    sensor.set_fifo_watermark_level(watermark)

    sensor.clear_buffer()                               # clear buffer values

    #
    # Turn on operating mode (disables setup)
    #


    sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    logger.info('Wakeup event with FIFO -trigger initialized.')


def read_with_polling(sensor):
    if sensor.WHOAMI in sensor._WAIS122:
        comp = 2  # KX122, big FIFO
    else:
        comp = 0  # KX022, smaller FIFO

    bufres = sensor.get_fifo_resolution()                       # buffer 0=8bit/1=16b

    bytes_to_read = buffer_size[comp + bufres]
    assert(watermark <= bytes_to_read)

    # time (ms) info
    odr_t = 1 / \
        hz[sensor.read_register(r.KX022_ODCNTL, 1)[0] &
           m.KX022_ODCNTL_OSA_MASK]

    pin_condition1 = 0
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        pin_condition1 = 1
    pin_condition2 = 0
    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        pin_condition2 = 1

    try:
        wu_event = False
        bfi_event = False

        sensor.clear_buffer()                               # clear buffer values

        while 1:
            # first check wu event
            if evkit_config.get('generic', 'use_adapter_int_pins') == 'TRUE':
                # Read int pin
                wufs = sensor._bus.poll_gpio(2) == pin_condition2
            else:
                # Read interrupt register
                wufs = sensor.read_register(r.KX022_INS2, 1)[
                    0] & b.KX022_INS2_WUFS > 0
                # alternative method to check triggering from registers
                #tds = sensor.read_register(r.KX022_BUF_STATUS_2, 1)[0] & b.KX022_BUF_STATUS_2_BUF_TRIG > 0

            if wufs:
                # print wu event and directions
                if not wu_event:
                    wu_direction = sensor.read_register(r.KX022_INS3)[0]
                    k = 0
                    wuf1 = 0  # last axis informed
                    for i in range(0, 6):
                        j = 0x01 << i
                        if wu_direction & j > 0:
                            k = k + 1
                            print 'WAKEUP DETECTION: MOVING #', k, "direction",
                            print resultResolverToString[j]
                            wuf1 = j
                    wu_event = True                                                 # wu happens

                # wait buffer full status
                print 'Waiting for FIFO to fill up'
                
                while not bfi_event:                    # wait for Buffer Full Interrupt
                    if evkit_config.get('generic', 'use_adapter_int_pins') == 'TRUE':
                        bfi_event = sensor._bus.poll_gpio(1) == pin_condition1
                    else:
                        bfi_event = sensor.read_register(r.KX022_INS2, 1)[
                            0] & b.KX022_INS2_BFI > 0
                    time.sleep(0.005)

                # flush buffer
                if wu_event and bfi_event:
                    import os
                    if not os.path.isdir("log"):
                        os.mkdir('log')

                    # FIXME does not work if multiple directions detected
                    file_out = 'log/%s_%s.txt' % (time.strftime(
                        '%m%d_%H%M%S'), wu_bits_to_str(wu_direction))

                    logger.info('flushing fifo to %s' % file_out)
                    fp = open(file_out, 'w')
                    timing.reset()

                    samples_in_multiread = 2  # TODO support for other values than 2
                    for i in range(0, bytes_to_read / samples_in_multiread):
                        # print 'fifo info', counter, sensor.get_fifo_level()
                        # time ref as seconds from start of buffer storage
                        now_s = i * odr_t * samples_in_multiread
                        if bufres:
                            buf_storage = sensor.read_register(
                                r.KX022_BUF_READ, 6 * samples_in_multiread)
                            x1, y1, z1, x2, y2, z2 = struct.unpack(
                                'hhhhhh', buf_storage)
                        else:
                            buf_storage = sensor.read_register(
                                r.KX022_BUF_READ, 3 * samples_in_multiread)
                            x1, y1, z1, x2, y2, z2 = struct.unpack(
                                'bbbbbb', buf_storage)
                        fp.write('%f%s%d%s%d%s%d\n' % (
                            now_s, DELIMITER, x1, DELIMITER, y2, DELIMITER, z1))
                        fp.write('%f%s%d%s%d%s%d\n' % (now_s + odr_t,
                                                       DELIMITER, x2, DELIMITER, y2, DELIMITER, z2))

                    fp.close()
                    logger.info('file ' + file_out + ' stored')
                    print 'FIFO flushed at %f seconds' % timing.time_elapsed()

                    # only one file log. Comment out if want to collect many
                    # log files.
                    break

                    wu_event = False
                    bfi_event = False
                    sensor.clear_buffer()                           # clear buffer values
                    sensor.release_interrupts()                     # int release
                else:
                    logger.error("no wu or buffer full interrupts")
                    break

    except KeyboardInterrupt:
        pass

    finally:
        sensor.clear_buffer()
        sensor.disable_fifo()


def app_main():
    sensor = kx022_driver()
    bus = open_bus_or_exit(sensor)

    enable_wu_w_trig_fifo(sensor, bres = BRES_8_BIT)
    # datalogging must be defined after wu since wu defines sensor's ODR
    enable_data_logging(sensor, 
    odr=1600,
    max_range='8G',
    lp_mode='NO_AVG'
    )

    if args.stream_mode:
        assert 0, 'Feature not implemented.'
    else:
        read_with_polling(sensor)

    sensor.set_power_off()
    bus.close()

if __name__ == '__main__':
    app_main()
