# 
# Copyright 2016 Kionix Inc.
#
from array import array, ArrayType
from bus_base import _spi_bus, _i2c_bus, BusException
from lib.util_lib import logger, evkit_config

aardvark_found = False
try:
    import aardvark_py as aa
    aardvark_found = True
except ImportError:
    # todo try to import linux aardvark if running in Linux environment
    raise
    pass

class bus_aadvark_i2c(_i2c_bus):
    # TODO demonstarte how to put sensor to hs mode
    aa_target_power = {
            'AA_TARGET_POWER_BOTH':aa.AA_TARGET_POWER_BOTH,
            'AA_TARGET_POWER_NONE':aa.AA_TARGET_POWER_NONE
            }
    aa_i2c_pullup = {
            'AA_I2C_PULLUP_BOTH':aa.AA_I2C_PULLUP_BOTH,
            'AA_I2C_PULLUP_NONE':aa.AA_I2C_PULLUP_NONE,
            }

    def __init__(self, aadvark_index = None ):
        _i2c_bus.__init__(self)
        self.bus_gpio_list = [1,2]
        self._has_gpio = True
        self._handle = None
        self._bitrate = None
        
        if not aardvark_found:
            raise BusException('Aardvark libraries not found/installed.')

        (num, ports, unique_ids) = aa.aa_find_devices_ext(16, 16)
        if ( num == 0 ):
            raise BusException('Aardvark i2c/spi host adapter not connected.')
        elif ( num == -2 ):
            raise BusException('Aardvark i2c/spi host adapter never connected.')
        else:
            self._ports = ports[0]
            if ( num > 1 ):
                logger.warning('More that 1 Aardvark ports found. Selecting 1st one.')

    def open(self, port_index=0):
        "Connect to bus adapter"
        _i2c_bus.open(self)

        # TODO, need to support multiple instances of bus_aadvark_i2c with single adapter.
        # This way it is possible to connect multiple i2c slaves to same bus.
        
        self._handle = aa.aa_open(port_index)
        if self._handle < 0:
            if ( self._handle == -7 ):
                raise BusException('bus_aadvark_i2c.open failed with error code %d (Aardvark disconnected)' % self._handle)
            else:
                raise BusException('bus_aadvark_i2c.open failed with error code %d' % self._handle)

        # IO direction now all input, do this before AA_CONFIG_GPIO_I2C
        aa.aa_gpio_direction(self._handle, int(evkit_config.get('aardvark_i2c', 'aa_gpio_direction'),16))

        ## select pullup or floating
        #aa.aa_gpio_pullup(self._handle, aa.AA_GPIO_SCK | aa.AA_GPIO_MOSI) # pullup for gpio lines
        aa.aa_gpio_pullup(self._handle, int(evkit_config.get('aardvark_i2c', 'aa_gpio_pullup'),16))

        #todo slave address selection GPIO to output

        # Ensure that the I2C subsystem is enabled
        aa.aa_configure(self._handle,  aa.AA_CONFIG_GPIO_I2C)
            
        # Enable the I2C bus pullup resistors (2.2k resistors).
        # This command is only effective on v2.0 hardware or greater.
        # The pullup resistors on the v1.02 hardware are enabled by default.
        aa.aa_i2c_pullup(self._handle, self.aa_i2c_pullup[evkit_config.get('aardvark_i2c', 'aa_i2c_pullup')])
        
        # Power the board using the Aardvark adapter's power supply.
        # This command is only effective on v2.0 hardware or greater.
        # The power pins on the v1.02 hardware are not enabled by default.
        aa.aa_target_power(self._handle, self.aa_target_power[evkit_config.get('aardvark_i2c','aa_target_power')])
            
        # Set the bitrate
        requested = self._bitrate
        self._bitrate = aa.aa_i2c_bitrate(self._handle, self._bitrate)
        if requested != self._bitrate:
            logger.warning('Bitrate set to %d kHz. Wanted to set %d kHz' % (self._bitrate, requested))

    def close(self):
        "Disconnect from bus adapter"
        _i2c_bus.close(self)

        assert self._handle >0,'Connection is already close.'
        aa.aa_close(self._handle)
        self._handle = None

    def poll_gpio(self, index):
        assert index in self.bus_gpio_list
        if index == 1:
            return (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SCK  ) > 0
        else:
            return (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_MOSI  ) > 0
    
    def _gpio_status(self):
        "Returns raw value of i2c adapter gpio lines"
        # AA_GPIO_SCK  = INT 1
        # AA_GPIO_MOSI = INT 2
        return aa.aa_gpio_get(self._handle) & (aa.AA_GPIO_SCK | aa.AA_GPIO_MOSI )
        
    def configure(self, cfg):
        self._bitrate = cfg['CLK_SPEED']

    def get_configuration_template(self):
        return {
            'CLK_SPEED':evkit_config.getint('i2c', 'bitrate'),
            'TIMEOUT':evkit_config.getint('i2c', 'bus_timeout')
            }
    
    def read_register(self, sensor, register, length=1):
        sad = self._sensortable[sensor]
        # todo check write status first
        aa.aa_i2c_write(self._handle, sad, aa.AA_I2C_NO_STOP, array('B', [register]))  # write address
        (count, data_in) = aa.aa_i2c_read(self._handle, sad, aa.AA_I2C_NO_FLAGS, length)    # read data
        if count != length:
            raise BusException('No response from I2C slave at address 0x%x for sensor %s' % (sad,sensor))

        return data_in

    def write_register(self, sensor, register, data):
        if isinstance(data, int):
            length = 2
            data_out = array('B', [register, data])
        elif isinstance(data,list) or isinstance(data,tuple):
            data = list(data)
            length = 1+len(data)
            data_out = array('B', [register] + data)
        else:
            raise BusException('Datatype "%s" not supported.' % type(data))
        
        sad = self._sensortable[sensor]
        res = aa.aa_i2c_write(self._handle, sad, aa.AA_I2C_NO_FLAGS, data_out)

        if res != length:
            raise BusException('Unable write to I2C slave at address 0x%x for sensor %s' % (sad,sensor))
            
    def get_status_string(self, res):
        return aa.aa_status_string(res)
    
class bus_aadvark_spi(_spi_bus):
    _polarity={'RISING_FALLING':aa.AA_SPI_POL_RISING_FALLING,
               'FALLING_RISING':aa.AA_SPI_POL_FALLING_RISING}

    _phase={'SETUP_SAMPLE':aa.AA_SPI_PHASE_SETUP_SAMPLE,
            'SAMPLE_SETUP':aa.AA_SPI_PHASE_SAMPLE_SETUP}

    _ss_polarity={'ACTIVE_HIGH':aa.AA_SPI_SS_ACTIVE_HIGH,
                  'ACTIVE_LOW':aa.AA_SPI_SS_ACTIVE_LOW}
    
    _bitorder={'MSB':aa.AA_SPI_BITORDER_MSB,
               'LSB':aa.AA_SPI_BITORDER_LSB}
    
    _aa_target_power={'AA_TARGET_POWER_BOTH':aa.AA_TARGET_POWER_BOTH,
                      'AA_TARGET_POWER_NONE':aa.AA_TARGET_POWER_NONE}
    
    def __init__(self):
        _spi_bus.__init__(self)
        self.bus_gpio_list = [1,2]
        self._has_gpio = True
        self._handle = None
        self._bitrate = None
        
        if not aardvark_found:
            raise BusException('Aardvark libraries not found/installed.')

        (num, ports, unique_ids) = aa.aa_find_devices_ext(16, 16)
        if ( num == 0 ):
            raise BusException('Aardvark i2c/spi host adapter not connected.')
        elif ( num == -2 ):
            raise BusException('Aardvark i2c/spi host adapter never connected.')
        else:
            self._ports = ports[0]
            if ( num > 1):
                logger.warning('More that 1 Aardvark ports found. Selecting 1st one.')

        self.MASKR           = int(evkit_config.get('spi','maskr'),2)    # SPI's read address mask

    def open(self, port_index=0):
        assert evkit_config.get('spi','ss_polarity') in ['ACTIVE_LOW','ACTIVE_HIGH']
        assert evkit_config.get('spi','bitorder') in ['MSB','LSB']
        _spi_bus.open(self)

        self._handle = aa.aa_open(port_index)
        if self._handle < 0:
            if ( self._handle == -7 ):
                raise BusException('bus_aadvark_spi.open failed with error code %d (Aardvark disconnected)' % self._handle)
            else:
                raise BusException('bus_aadvark_spi.open failed with error code %d' % self._handle)
        
        aa.aa_gpio_direction(self._handle,int(evkit_config.get('aardvark_spi', 'aa_gpio_direction'),16)) # IO direction 

        ## select pullup or floating
        #aa.aa_gpio_pullup(self._handle, aa.AA_GPIO_SCL | aa.AA_GPIO_SDA)             # pullup
        aa.aa_gpio_pullup(self._handle, int(evkit_config.get('aardvark_spi', 'aa_gpio_pullup'),16))

        aa.aa_configure(self._handle,aa.AA_CONFIG_SPI_GPIO) # SPI subsystem is enabled
        
        aa.aa_target_power(self._handle, self._aa_target_power[evkit_config.get('aardvark_spi','aa_target_power')])
                           
        aa.aa_spi_configure(self._handle,
                            self._cpol,
                            self._cpha,
                            self._bitorder[evkit_config.get('spi','bitorder')]
                            )

        aa.aa_spi_master_ss_polarity(self._handle,
                                     self._ss_polarity[evkit_config.get('spi','ss_polarity')])

        requested = self._bitrate
        self._bitrate = aa.aa_spi_bitrate(self._handle, self._bitrate) # Set the bitrate

        if requested != self._bitrate:
            logger.warning("Warning Bitrate set to %d kHz. Wanted to set %d kHz" % (self._bitrate, requested))

    def close(self):
        "Disconnect from bus adapter"
        _spi_bus.close(self)        

        assert self._handle > 0,'Connection is already close.'
        aa.aa_close(self._handle)
        self._handle = None

    def configure(self, cfg):
        self._cpol = cfg['SPI_CPOL']
        self._cpha = cfg['SPI_CPHA']
        self._bitrate = cfg['SPI_BITRATE']

    def get_configuration_template(self):
        assert evkit_config.get('spi','polarity') in ['RISING_FALLING','FALLING_RISING']
        assert evkit_config.get('spi','phase') in ['SAMPLE_SETUP','SETUP_SAMPLE']

        return {
            'SPI_CPOL': self._polarity[evkit_config.get('spi','polarity')],
            'SPI_CPHA': self._phase[evkit_config.get('spi','phase')],
            'SPI_BITRATE':evkit_config.getint('spi', 'bitrate'), # MAX value for Aardvark
            }

    def write_register(self, sensor, register, data):
        if register is None:        # Pure SPI command write without address
            data_out = array('B', [data])
            length = 1 ## FIXME len(data)
        elif isinstance(data, int): # normal address set and data write
            length = 2  ## FIXME multiwrite
            data_out = array('B', [register, data])
        else:
            raise BusException('Datatype "%s" not supported.' % type(data))
          
        # todo check sensor chip select parameters from self._sensortable
        res, dummy_data = aa.aa_spi_write(self._handle, data_out, 0)  # write the reg.address and data
        if res != length:
            raise BusException('Unable write to SPI slave.')


    def read_register(self, sensor, register, length=1):
        data_in  = aa.array_u08(1 + length)
        data_out = array('B', [0 for i in range(1 + length) ] )
        data_out[0] = register | self.MASKR

        try:        
            (count, data_in)  = aa.aa_spi_write(self._handle, data_out, data_in)  # write address
        except TypeError:
            raise BusException('Cannot read sensor from SPI bus.')
        
        #logger.debug( 'count,length %d %d ' %(count,length))
        assert count == length+1
        return data_in[1:]

    def poll_gpio(self, index):
        # AA_GPIO_SCL, AA_GPIO_SDA
        assert index in self.bus_gpio_list

        if index == 1: # int 1
            return (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SCL  ) > 0
        else: # int 2
            return (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SDA  ) > 0
    
    def _gpio_status(self):
        # AA_GPIO_SCL = INT 2
        # AA_GPIO_SDA = INT 1
        return aa.aa_gpio_get(self._handle) & (aa.AA_GPIO_SCL | aa.AA_GPIO_SDA )
        
