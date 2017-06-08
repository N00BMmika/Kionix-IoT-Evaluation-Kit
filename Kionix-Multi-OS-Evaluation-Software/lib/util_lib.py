# 
# Copyright 2016 Kionix Inc.
#
import time
from array import array, ArrayType
import struct
import logging as __logging
import sys

#TODO move logger spesific arguments somewhere else
import argparse as __argparse
_argparser = __argparse.ArgumentParser(description='Example: %(prog)s -s')
_argparser.add_argument('-l','--loop',default=None,type=int, help='How many samples to read in loop (default None = infinite loop).')
_argparser.add_argument('-s','--stream_mode',action='store_true', help='Use high speed streaming mode (not active by default)')
_argparser.add_argument('-x','--streamfile',action='store_true')
args = _argparser.parse_args()

from datetime import datetime

#common timing class definition
class Timing_datetime:
    def __init__(self):
        self.reset()

    def reset(self):
        self.starttime = datetime.now()
        
    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return (datetime.now()-self.starttime).total_seconds()

class Timing_time:
    def __init__(self):
        self.reset()

    def reset(self):
        self.starttime = time.clock()
        
    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return (time.clock()-self.starttime)

#instance for timing class.
if sys.platform.startswith('win'):
    timing = Timing_time() # windows
else:
    timing = Timing_datetime() # Linux

import ConfigParser
evkit_config = ConfigParser.RawConfigParser()
evkit_config.read(['../settings.cfg','settings.cfg', 'port.cfg']) # try to find cfg from different locations


log_level_dict={
    'DEBUG': __logging.DEBUG,
    'INFO': __logging.INFO,
    'WARNING':__logging.WARNING,
    'ERROR': __logging.ERROR,
    'CRITICAL': __logging.CRITICAL,
    }

#TODO add command line paramter for changing log level
logger = __logging.getLogger(__name__)
logger.setLevel(log_level_dict[evkit_config.get('generic', 'logging_level')])

#formatter = __logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# change verbose level of log messages based on logging level
if evkit_config.get('generic', 'logging_level') in ['DEBUG']:
    formatter = __logging.Formatter('%(levelname)s :\t%(filename)s (%(lineno)d) :\t%(funcName)s :\t%(message)s')
else:
    formatter = __logging.Formatter('%(levelname)s :\t%(message)s')


if evkit_config.get('generic', 'log_file'):
    fh = __logging.FileHandler(evkit_config.get('generic', 'log_file'),
                             mode='w' # overwrite
                             )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

if evkit_config.getint('generic', 'log_to_console'):
    ch = __logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

##logger.debug('Debug level active')
##logger.info('Info Level Active')
##logger.warning('Warning level Active')
##logger.error('Error level active')
##logger.critical('Critical level active')

def stream_config_check():

    if not(evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT','ADAPTER_GPIO2_INT']):
        return 'Stream mode requires GPIO drdy_operation in settings.cfg'

    if not ( evkit_config.get('connection', 'bus_index') in ['3','5'] or  \
           evkit_config.get('connection', 'bus_index').startswith('serial_')):
        return 'Stream mode requires serial connection or connection type 3 or 5 in settings.cfg'

    return True
           


# http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-being-interrupted-by-keyboardinterrupt-in-py
import signal

class DelayedKeyboardInterrupt(object):
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        #logger.debug('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)

#definitions for channels
CH_ACC, CH_MAG, CH_GYRO, CH_TEMP, CH_SLAVE1, CH_SLAVE2 = [2**t for t in range(6)]

def delay_seconds(seconds):
    time.sleep(seconds)

def bin2uint16(data):
    return data[0] | data[1] << 8

def bin2uint8(data):
    if isinstance(data, array):
        data=data[0]
    return data 

# convert int and float to string which is used in enumerated values dictionaries
def convert_to_enumkey(value):
    if isinstance(value,int):
        value = str(value)
    elif isinstance(value,float):
        value = str(value)
        value=value.replace('.','p')
    elif isinstance(value,str):
        pass
    else:
        assert 0,'Invalid enumkey'
    return value

# delimiter character for log printout
DELIMITER = ';\t'
