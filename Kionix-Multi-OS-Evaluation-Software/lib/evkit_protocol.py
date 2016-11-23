# 
# Copyright 2016 Kionix Inc.
#
"""Evkit microcontroller base protocol definitions for kionix command line evaluation kit
"""
from lib.bus_base import BusException
from struct import pack, unpack
from util_lib import logger

EVKIT_ERROR_BASE_NUM                                    = 0x00

EVKIT_SUCCESS                                           = (EVKIT_ERROR_BASE_NUM + 0)  
EVKIT_BUS1_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 1)  
EVKIT_BUS2_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 2)  
EVKIT_GPIO_INVALID                                      = (EVKIT_ERROR_BASE_NUM + 3)  
EVKIT_GPIO_RESERVED                                     = (EVKIT_ERROR_BASE_NUM + 4)  
EVKIT_MAX_GPIO_RESERVED                                 = (EVKIT_ERROR_BASE_NUM + 5)  
EVKIT_MAX_EXE_PARAMS_ERROR                              = (EVKIT_ERROR_BASE_NUM + 6)
EVKIT_INTERRUPT_WAITING                                 = (EVKIT_ERROR_BASE_NUM + 7)  
EVKIT_INTERRUPT_DETECTED                                = (EVKIT_ERROR_BASE_NUM + 8)  
EVKIT_DATA_READ_ERROR                                   = (EVKIT_ERROR_BASE_NUM + 9)  
EVKIT_DATA_STREAM_ACTIVE                                = (EVKIT_ERROR_BASE_NUM + 10)
EVKIT_GPIO_STATUS_READ_ERROR                            = (EVKIT_ERROR_BASE_NUM + 11)
EVKIT_MSG_LENGHT_ERROR                                  = (EVKIT_ERROR_BASE_NUM + 12)
EVKIT_BUS2_BUFFER_FULL                                  = (EVKIT_ERROR_BASE_NUM + 13)

EVKIT_MSG_MAX_PAYLOAD_SIZE                              = 0x0c # size in bytes 12
EVKIT_MSG_MAX_PAYLOAD_IND_SIZE                          = 0x12 # size in bytes 18
EVKIT_MSG_MAX_EXE_PARAMS                                = 0x04
EVKIT_MSG_MAX_GPIO                                      = 0x04

EVKIT_MSG_HEADER_LENGH                                  = 0x02
EVKIT_MSG_BUS_PARAMS_LENGH                              = 0x02

EVKIT_MSG_GPIO_PIN_NOSENSE                              = 0x00
EVKIT_MSG_GPIO_PIN_SENSE_LOW                            = 0x01
EVKIT_MSG_GPIO_PIN_SENSE_HIGH                           = 0x02  

EVKIT_MSG_GPIO_PIN_NOPULL                               = 0x00
EVKIT_MSG_GPIO_PIN_PULLDOWN                             = 0x01
EVKIT_MSG_GPIO_PIN_PULLUP                               = 0x02

EVKIT_MSG_READ_REQ                                      = 0x01
EVKIT_MSG_READ_RESP                                     = 0x02

EVKIT_MSG_WRITE_REQ                                     = 0x03
EVKIT_MSG_WRITE_RESP                                    = 0x04

EVKIT_MSG_VERSION_REQ                                   = 0x05
EVKIT_MSG_VERSION_RESP                                  = 0x06

EVKIT_MSG_ENABLE_INT_REQ						    = 0x07
EVKIT_MSG_ENABLE_INT_RESP	  					    = 0x08

EVKIT_MSG_DISABLE_INT_REQ						    = 0x09
EVKIT_MSG_DISABLE_INT_RESP	 					    = 0x10


EVKIT_MSG_GPIO_STATE_REQ                                = 0x0E
EVKIT_MSG_GPIO_STATE_RESP                               = 0x0F

EVKIT_MSG_ERROR_IND                                     = 0x11

EVKIT_GPIO_PIN_NOSENSE                              = 0x00
EVKIT_GPIO_PIN_SENSE_LOW					        = 0x01
EVKIT_GPIO_PIN_SENSE_HIGH					        = 0x02  

EVKIT_GPIO_PIN_NOPULL					     		= 0x00
EVKIT_GPIO_PIN_PULLDOWN				      		    = 0x01
EVKIT_GPIO_PIN_PULLUP					     		= 0x02


EVKIT_MSG_INTERRUPT_IND1 							= 0x0A
EVKIT_MSG_INTERRUPT_IND2 							= 0x0B
EVKIT_MSG_INTERRUPT_IND3 							= 0x0C
EVKIT_MSG_INTERRUPT_IND4 							= 0x0D

EVKIT_GPIO_PIN_SENSE_LOW					        = 0x01
EVKIT_GPIO_PIN_PULLUP					     		= 0x02

class ProtocolException(Exception): pass
            
class evkit_incoming_msg(object):

    def __init__(self, data):
        assert len(data)>1,'Incoming message too short'
        self._position = 0
        self._data = data

    def value(self):
        value = self._data[self._position]
        self._position+= 1
        return ord(value)

    def value_block(self, lenght):
        #fixme lenght check
        values = self._data[self._position:self._position+lenght]
        self._position = self._position + lenght
        return values

    def get_msg_type(self):
        return self._data[0]

    def verify_message_type(self, msg_type):
        if self.get_msg_type() != msg_type:
            raise ProtocolException('Wrong message type %x received' % msg_type)
        
class evkit_outgoing_msg(object):
    def __init__(self):
        self._data = ''

    def value(self, values):
        if isinstance(values, int):
            values = [values]
        
        for value in values:
            self._data+=chr(value)
        return self
    
    def get_message(self):
        self._data=chr(len(self._data)+1)+self._data
        #print '<msg>%s</msg>' % ','.join([str(ord(t)) for t in self._data])
        return self._data
    
class evkit_handle_protcol_msg(object):

    def version_req(self):
        msg = evkit_outgoing_msg() \
            .value(EVKIT_MSG_VERSION_REQ) \
            .get_message()
        return msg

    def handle_version_resp(self, data):
        msg = evkit_incoming_msg(data)
        msg_type = msg.value()
        if EVKIT_MSG_VERSION_RESP == msg_type:
            status = msg.value()
            if EVKIT_SUCCESS != status:
                raise ProtocolException('Version request failure %d' % status)
            #else:
                #TODO: Version number check, not needed yet
        else:
            #print 'message is', ''.join('0x%02x,' % ord(t) for t in msg._data)
            raise ProtocolException('Version request wrong message type %d' % msg_type)
        return status

    def write_req(self, sad, register, value):
        data = evkit_outgoing_msg().value(EVKIT_MSG_WRITE_REQ) \
            .value(sad) \
            .value(register) \
            .value(value) \
            .get_message()
        assert len(data)<=20,'Message length too big. Length is %d' % len (data)
        return data
    
    def interrupt_disable_req(self, pin,
                              sense = EVKIT_GPIO_PIN_SENSE_LOW,
                              pull = EVKIT_GPIO_PIN_PULLUP):
        
        data = evkit_outgoing_msg() \
                .value(EVKIT_MSG_DISABLE_INT_REQ) \
                .value(pin) \
                .value(sense) \
                .value(pull).get_message()

        #print 'interrupt_disable_req', [hex(ord(t)) for t in data]
        return data

    def interrupt_enable_req(self,pin, payload_definition,
                             sense = EVKIT_GPIO_PIN_SENSE_LOW,
                             pull = EVKIT_GPIO_PIN_PULLUP
                             ):
        data_list = [5+len(payload_definition), EVKIT_MSG_ENABLE_INT_REQ, pin, sense, pull]+payload_definition
        fmt = 'b'*len(data_list)
        data = pack(fmt,*data_list)
##        print '<start_msg>%s</start_msg>' % ','.join([str(ord(t)) for t in data])
        return data

##        data = evkit_outgoing_msg()\
##               .value(EVKIT_MSG_ENABLE_INT_REQ) \
##               .value(pin) \
##               .value(sense) \
##               .value(pull) \
##               .value(sad) \
##               .value(register) \
##               .value(length).get_message()
##        #print 'interrupt_enable_req', [hex(ord(t)) for t in data]
##        return data

##    def interrupt_enable_req_9d(self,pin, value_array):
##        data = evkit_outgoing_msg()\
##               .value(EVKIT_MSG_ENABLE_INT_REQ) \
##               .value(pin)  \
##               .value(0x01) \
##               .value(0x02) \
##               .value_array(value_array).get_message()
##        return data
    
    def handle_write_resp(self, data):
        msg = evkit_incoming_msg(data)
        msg_type = msg.value()
        if EVKIT_MSG_WRITE_RESP == msg_type:
            sad = msg.value()
            register = msg.value()
            status = msg.value()
            if EVKIT_SUCCESS != status:
                raise ProtocolException('Write request failure %d' % status)
            return status
        # TODO : wrong message can be received when stopping streaming mode.
        #raise ProtocolException,'Wrong message type received 0x%02x' % msg_type
        logger.warning('Wrong message type received 0x%02x' % msg_type )
    
    def read_req(self, sad, register, length=1):
        data= evkit_outgoing_msg().value(EVKIT_MSG_READ_REQ) \
            .value(sad) \
            .value(register) \
            .value(length) \
            .get_message()
        return data
    
    def handle_read_resp(self, data,lenght):
        msg = evkit_incoming_msg(data)
        msg_type = msg.value()
        if EVKIT_MSG_READ_RESP == msg_type:
            sad = msg.value()
            register = msg.value()
            status = msg.value()
            if EVKIT_SUCCESS != status:
                raise BusException('Read request failure: %s' % status)
        return msg.value_block(lenght)
    
    def gpio_state_req(self, gpio_nrb):
        msg = evkit_outgoing_msg().value(EVKIT_MSG_GPIO_STATE_REQ) \
            .value(gpio_nrb) \
            .get_message() 
        return msg
    
    def handle_gpio_state_resp(self, data):
        msg = evkit_incoming_msg(data)
        msg_type = msg.value()
        if EVKIT_MSG_GPIO_STATE_RESP == msg_type:
            gpio_nrb = msg.value()
            gpio_sense = msg.value()
            status = msg.value()
            if EVKIT_SUCCESS != status:
                raise ProtocolException('Gpio state read failure %d' % status)
        if EVKIT_MSG_GPIO_PIN_SENSE_HIGH == gpio_sense:
            sense = 1
        else:
            sense = 0
        return sense

    def handle_interrupt_enable_resp(self, data):
        "Returns EVKIT_MSG_INTERRUPT_IND? index number"
        if len(data)!=3: ProtocolException('Wrong packet lenght %d.' % len(data))

        msg_id, msg_data, msg_status  = unpack('bbb',data)
        
        if msg_id != EVKIT_MSG_ENABLE_INT_RESP:
            raise ProtocolException('Wrong message type %x received' % msg_id)
        
        if msg_status != EVKIT_SUCCESS:
            raise ProtocolException('request failed %x' % msg_status)
        
        return msg_data
