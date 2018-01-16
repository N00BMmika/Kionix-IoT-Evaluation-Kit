# 
# Copyright 2016 Kionix Inc.
#
import struct
import time
import types
from lib.util_lib import DELIMITER, evkit_config, logger, timing
from lib.bus_base import BusException

import traceback, os
NEW_LINE='\n'
    
class ext:
    "Extra data what can be subscribed in stream request messages"
    reg_packet_count_8 = [0xff,0x00,0x00]
    hdr_packet_count_8 = '!ind'
    fmt_packet_count_8 = 'B'

def timenow_str():
    return time.strftime('%Y-%m-%d %H:%M:%S:000')

def start_time_str():
    caller = ''
    try:
        caller = os.path.split(traceback.extract_stack()[0][0])[1]
    except:
        caller = ''
    return '# Log File Format Version = 1.0\n# Stream Configuration File = %s\n# Start time = %s' % (caller, timenow_str())

def end_time_str():
    return '# End time = ' + timenow_str()

class request_message_definition(object):
    def __init__(self, sensor, fmt, hdr, reg, pin_index):
        self.msg_fmt = fmt
        self.msg_hdr = hdr
        self.py_headerstr = '#timestamp%s%s' % (DELIMITER, self.msg_hdr.replace('!',DELIMITER))
        self.sensor = sensor
        self.reg = reg
        self.pin_index = pin_index
        self.gpio_pin = None
        self.msg_size = None
        self.msg_req = None

    def __str__(self):
        return 'request_message_definition %s' % self.py_headerstr
    
class stream_config:
    def __init__(self, sensor=None):
        # if sensor not defined here then must be defined on define_request_message()
        # FIXME does not work if sensor not defined here
        self.sensor = sensor
        self.request_message_list=[] # list of all data streams requested
        self.msg_ind_dict = {}       #  

    def define_request_message(self, sensor=None, fmt=None, hdr=None, reg=None, pin_index=None):
        # NOTE : =None needed due API change and to prevent API break
        if sensor is not None:
            message = request_message_definition(sensor, fmt, hdr, reg, pin_index)
        else:
            message = request_message_definition(self.sensor, fmt, hdr, reg, pin_index)
        self.request_message_list.append(message)        
        self.prepare_request_message(message)
        
    def prepare_request_message(self, message):
        message.gpio_pin = message.sensor._bus._gpio_pin_index[message.pin_index]
        
        # uses self.msg_size-1 because channel number will be added to response
        # (it is not included in payload)
        message.msg_size = struct.calcsize(message.msg_fmt)

        assert type(message.reg) in [int, list],'Register variable type must be int or list.'
        
        # simple way to define what to read
        if isinstance(message.reg, int):
            message.msg_req = [message.gpio_pin,
                               [message.sensor.address(),
                                message.reg,
                                message.msg_size-1]]

        else:
            # Advanced way. "Manual" definition of request payload
            message.msg_req = [message.gpio_pin, message.reg]

    def _start_streaming(self):
        # send stream start requests to FW
        logger.debug(">Enable interrupt request")
        for request in self.request_message_list:
            resp=self.sensor._bus.enable_interrupt(*request.msg_req)
            self.msg_ind_dict[resp] = request
        logger.debug("<Enable interrupt request")

    def _stop_streaming(self):

        logger.debug(">Disable interrupt request")
            
        self.sensor._bus._flush_input()        

        # send stream stop requests to FW in reversed order
        for request in reversed(self.request_message_list):
            self.sensor._bus.disable_interrupt(request.gpio_pin)

        self.sensor._bus._flush_input()        

        logger.debug("<Disable interrupt request")
   
    def read_data_stream(self,
                         loop = None,
                         console = True,
                         log_file_name = None,
                         callback = None,
                         max_timeout_count = 0,
                         additional_info = None):

        # set max_timeout_count to None if infinite amount of timeout allowed
        
        count = 0               # count of received data samples
        timeout_count = 0       # how many timeouts received
        file = None             # handle to file 

        # create file object form string or function which generates file name
        if isinstance(log_file_name, types.StringType):
            file = open(log_file_name,'w')

        # log_file_name is types.FunctionType if providing function which generates file name
        elif isinstance(log_file_name, types.FunctionType):
            file = open(log_file_name(),'w')

        # subscribe sensor data from FW
        self._start_streaming()
        timing.reset()
        
        if console:
            print (start_time_str())
            
        if file:
            file.write(start_time_str()+NEW_LINE)
            if additional_info: file.write('# Additional information = '+additional_info+NEW_LINE)   #optional: more information about the logging setup
            
        # print out header text, replace text "ch" with channel number
        for channel, request in self.msg_ind_dict.iteritems():
            if console:
                print (request.py_headerstr.replace('ch', str(channel)))
                
            if file:
                file.write(request.py_headerstr.replace('ch', str(channel))+NEW_LINE)
        try:
            # main loop for reading the data
            while count < loop or loop is None:
                resp = self.sensor._bus.wait_indication()

                if resp is None:
                    logger.debug("Timeout when receiving data")
                    timeout_count += 1
                    
                    if max_timeout_count is not None \
                       and timeout_count >= max_timeout_count:
                           
                        raise BusException('Timeout when receiving data. Max timeout count reached.')
                    
                    continue 

                # find correct message type to get information how message is interpreted
                # resp[0] has the channel number

                received_messsage_type = self.msg_ind_dict[resp[0]]

                if len(resp) !=received_messsage_type.msg_size:
                    logger.warning("Wrong message length %d" % len(resp) )
                else:
                    now = timing.time_elapsed()
                    data = struct.unpack(received_messsage_type.msg_fmt, resp)
                    text = '{:.6f}{}'.format(now, DELIMITER)

                    # TODO support for float values
                    text += DELIMITER.join('{:d}'.format(t) for t in data)
                    
                    if console:
                        print (text)
                        
                    if file:
                        file.write(text+NEW_LINE)
                    
                    count += 1
                
                if callback is not None:
                    # callback function returns False if need to stop reading
                    if callback(data) == False:
                        break

        except KeyboardInterrupt:
            # CTRL+C will stop data reading
            pass
        
        finally:
            # after CTRL+C or other exception, print end time stamp and stop reading sensor data
            if console:
                print (end_time_str())
                
            if file:
                file.write(end_time_str()+NEW_LINE)
                file.close()
                    
            # unsibscribe data from FW
            self._stop_streaming()

            if count==0:
                logger.error("No stream data received.")

