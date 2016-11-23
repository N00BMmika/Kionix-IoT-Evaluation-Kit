# 
# Copyright 2016 Kionix Inc.
#
from bus_base import _i2c_bus, BusException
from socket_sender import  SocketSender
from util_lib import logger, DelayedKeyboardInterrupt, evkit_config
from time import sleep

from evkit_protocol import evkit_handle_protcol_msg, ProtocolException

from socket_connection import SocketTimeoutException
import array

class bus_adb_socket(_i2c_bus):
    def __init__(self):
        _i2c_bus.__init__(self)
        self._status = 0
        self._has_gpio = False
        self.bus_gpio_list = []
        self._gpio_pin_index = []

        self._message_handler = evkit_handle_protcol_msg()
        self._configure_interrupts()

    def _configure_interrupts(self):
        self.bus_gpio_list = []
        self._gpio_pin_index = []

        for t in range(1,4):
            if not evkit_config.has_option('protocol_gpio','pin%d_index' % t):
                break
            self._has_gpio = True
            self.bus_gpio_list.append(t)
            self._gpio_pin_index.append(evkit_config.getint('protocol_gpio','pin%d_index' % t))

        
    def configure(self, cfg):
        pass

    def get_configuration_template(self):
        return {}
  
    def open(self):
        assert (self._is_open == False)

        self.socketSender = SocketSender()
        self.socketSender._prepareSocketConnection()

        if not self.socketSender.isOpen():
            return False

        self._is_open = True
        data = self._message_handler.version_req()
        self.socketSender.sendMessage(data)
        self._flush_input()
        self.socketSender.sendMessage(data)
        
        try:
            socketMessage = self.socketSender.receiveMessage(timeout = 2)
        except SocketTimeoutException, err:
            raise BusException("Connection timeout")

        self._message_handler.handle_version_resp(socketMessage)
        self._flush_input()


    def _flush_input(self):
        while 1:
            with DelayedKeyboardInterrupt():
                sleep(0.05)
                try:
                    resp = self.socketSender.receiveMessage(timeout = 0.05)
                except SocketTimeoutException, err:
                    return
                
                if len(resp)==0: break                
                logger.debug('Flushing socket input.')
                        
    def wait_indication(self, timeout = 1):
        try:
            with DelayedKeyboardInterrupt():
                resp = self.socketSender.receiveMessage(timeout = timeout)
                
        except SocketTimeoutException:
            return None

        arr=array.array('B')
        arr.fromstring(resp)
        return arr

    def enable_interrupt(self, pin, payload_definition):
        data = self._message_handler.interrupt_enable_req(pin, payload_definition)
        self.socketSender.sendMessage(data)

        try:
            with DelayedKeyboardInterrupt():
                resp = self.socketSender.receiveMessage(timeout = 2)
                
        except SocketTimeoutException, err:
            raise BusException(err)        

        return self._message_handler.handle_interrupt_enable_resp(resp)
    
    def disable_interrupt(self, pin):
        data = self._message_handler.interrupt_disable_req(pin)
        self.socketSender.sendMessage(data)

        try:
            with DelayedKeyboardInterrupt():
                resp = self.socketSender.receiveMessage(timeout = 2)
                
        except SocketTimeoutException, err:
            raise BusException(err)        

        arr=array.array('B')
        arr.fromstring(resp)
        # TODO sometimes still receiving one stream message after disabled

        self._flush_input()
        return arr

    def read_register(self,sensor, register, length=1):
        sad = self._sensortable[sensor]
        
        data = self._message_handler.read_req(sad,register,length)        
        self.socketSender.sendMessage(data)

        try:
            with DelayedKeyboardInterrupt():
                resp = self.socketSender.receiveMessage(timeout = 2)
                
        except SocketTimeoutException, err:
            raise BusException(err)        
        resp = self._message_handler.handle_read_resp(resp,length)
        arr=array.array('B')
        arr.fromstring(resp)
        return arr
    
    def write_register(self, sensor, register, value):
        sad = self._sensortable[sensor]

        data = self._message_handler.write_req(sad,register,value)

        with DelayedKeyboardInterrupt():
            self.socketSender.sendMessage(data)
            resp = self.socketSender.receiveMessage()

        return self._message_handler.handle_write_resp(resp)

    def gpio_read(self, gpio):        
        data = self._message_handler.gpio_state_req(gpio)

        with DelayedKeyboardInterrupt():
            self.socketSender.sendMessage(data)
            resp = self.socketSender.receiveMessage()        

        return self._message_handler.handle_gpio_state_resp(resp)
    
    def poll_gpio(self, index):
        assert index in self.bus_gpio_list
        return self.gpio_read(self._gpio_pin_index[index-1])
    
    def close(self):
        assert (self._is_open == True)
        self._is_open = False
