# 
# Copyright 2016 Kionix Inc.
#
import struct
import time
from lib.util_lib import DELIMITER, evkit_config, logger, timing
import traceback, os

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
    
class stream_config:
    def __init__(self):
        self.request_message_list=[] # list of all data streams requested
        self.msg_ind_dict = {}       #  

    def define_request_message(self, sensor, fmt, hdr, reg, pin_index):
        message = request_message_definition(sensor, fmt, hdr, reg, pin_index)
        self.request_message_list.append(message)        
        self.prepare_request_message(message)
        
    def prepare_request_message(self, message):
        assert evkit_config.get('generic', 'drdy_operation') in ['ADAPTER_GPIO1_INT', 'ADAPTER_GPIO2_INT'], \
        'An Int pin must be configured in order to use streaming.'
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
            
    def read_data_stream(self, sensor, loop, callback = None):
        count = 0
        data_received = False
        
        # send stream start requests to FW
        for request in self.request_message_list:
            resp=sensor._bus.enable_interrupt(*request.msg_req)
            self.msg_ind_dict[resp] = request

        print start_time_str()
        
        # print out header text, replace text "ch" with channel number
        for channel, request in self.msg_ind_dict.iteritems():
            print request.py_headerstr.replace('ch', str(channel))

        try:

            while count < loop or loop is None:
                resp = sensor._bus.wait_indication()
                now = timing.time_elapsed()

                if resp is None:
                    logger.warning("timeout")

                # find correct message type to get information how message is interpreted
                # resp[0] has the channel number
                received_messsage_type = self.msg_ind_dict[resp[0]]

                if len(resp) !=received_messsage_type.msg_size:
                    logger.warning("Wrong message length %d" % len(resp) )
                else:
                    data_received = True
                    data = struct.unpack(received_messsage_type.msg_fmt, resp)
                    text = '{:.6f}{}'.format(now, DELIMITER)
                    text += DELIMITER.join('{:d}'.format(t) for t in data)
                    
                    print text
                    
                count += 1
                
                if callback is not None:
                    callback(resp)

        except KeyboardInterrupt:
            print end_time_str()
            pass
        
        finally:
            if not data_received:
                logger.error("No stream data received")
                
            logger.debug("Disable interrupt request")
            sensor._bus._flush_input()        

            # send stream stop requests to FW in reversed order
            for request in reversed(self.request_message_list):
                sensor._bus.disable_interrupt(request.gpio_pin)

            logger.debug("Disable interrupt done")
            