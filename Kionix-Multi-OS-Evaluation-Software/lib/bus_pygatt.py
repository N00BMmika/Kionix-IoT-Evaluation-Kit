# 
# Copyright 2016 Kionix Inc.
#
from time import sleep
import array
import os

from bus_base import _i2c_bus, BusException
from bus_evkit import kx_protocol_bus
from util_lib import logger, DelayedKeyboardInterrupt, evkit_config
import proto

class bus_linux_ble(kx_protocol_bus):
    def __init__(self, index = None ):
        # FIXME consider removing index
        kx_protocol_bus.__init__(self)        
        self.config_section = 'linux_ble' 
        self._configure_interrupts()

    def _configure_interrupts(self):
        # add all defined GPIO pins
        self.bus_gpio_list = []
        self._gpio_pin_index = []
        for t in range(1,4):
            if not evkit_config.has_option(self.config_section,'pin%d_index' % t):
                break
            self._has_gpio = True
            self.bus_gpio_list.append(t)
            self._gpio_pin_index.append(evkit_config.getint(self.config_section,'pin%d_index' % t))

        drdy_op = evkit_config.get('generic', 'drdy_operation') # Warn user if using interrupts and interrupt pin list is empty
        if self.bus_gpio_list == [] and drdy_op.startswith('ADAPTER_GPIO') :
            logger.critical('No interrupt pins configured in setting.cfg!')

    def open(self):
        import pygatt
        kx_protocol_bus.open(self)
        mac_addr = evkit_config.get(self.config_section, 'mac_address')
        logger.info('Connecting to MAC address %s' % mac_addr)

        self._kx_port = proto.pygatt_com(mac_addr) ####kx_com_port(comport,baudrate, timeout = 1)
        self._kx_connection = proto.ProtocolEngine(self._kx_port)

        # run version request
        # FIXME improve
        try:
            self.send_message(proto.version_req())
            response_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)        
            message_type, major_version, minor_version = proto.unpack_response_data(response_data)
        except Exception,e:
            # retry if error
            logger.debug('Version REQ failed. Flushing data and retry.')
            sleep(0.1)
            self._kx_port.flush()
            sleep(0.1)
            self.send_message(proto.version_req())
            response_data = self.receive_message(proto.EVKIT_MSG_VERSION_RESP)
            message_type, major_version, minor_version = proto.unpack_response_data(response_data)

        self.verify_protocol_version(major_version, minor_version)
        
