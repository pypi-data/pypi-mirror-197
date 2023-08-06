""" i2c communications for ES100

Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
"""

import time

try:
    from smbus import SMBus
except ModuleNotFoundError:
    SMBus = None

class ES100I2CError(Exception):
    """ ES100I2CError """

class ES100I2C:
    """ ES100I2C """

    ERROR_DELAY_SEC = 0.001             # 1 ms delay if i2c read/write error

    def __init__(self, bus, address, debug=False):
        """ __init__ """
        self._smbus = None
        if not SMBus:
            raise ES100I2CError('SMBus package not installed - are you on a Raspberry Pi?')
        self._debug = debug
        self._i2c_bus = bus
        self._i2c_address = address
        if self._i2c_bus < 0 or self._i2c_bus > 999:
            raise ES100I2CError('i2c bus number error: %s' % bus)
        if self._i2c_address < 0 or self._i2c_address > 127:
            raise ES100I2CError('i2c address number error: %s' % address)
        self.open()

    def __del__(self):
        """ __del__ """
        if not SMBus:
            return
        self.close()

    def open(self):
        """ _setup """
        if self._smbus:
            return
        try:
            self._smbus = SMBus(self._i2c_bus)
            #self._smbus.open(self._i2c_bus) # not needed if passed on class creation
        except FileNotFoundError as err:
            raise ES100I2CError('i2c bus %d open error: %s' % (self._i2c_bus, err)) from err

    def close(self):
        """ _close """
        if self._smbus:
            self._smbus.close()
            self._smbus = None

    def read(self):
        """ read """
        count = 0
        while True:
            try:
                rval = self._smbus.read_byte(self._i2c_address)
                return rval
            except (OSError, IOError) as err:
                if count > 10:
                    raise ES100I2CError('i2c read: %s' % (err)) from err
            time.sleep(ES100I2C.ERROR_DELAY_SEC)
            count += 1

    def write_addr(self, addr, data):
        """ write_addr """
        count = 0
        while True:
            try:
                self._smbus.write_byte_data(self._i2c_address, addr, data)
                return
            except (OSError, IOError) as err:
                if count > 10:
                    raise ES100I2CError('i2c write 0x%02x: %s' % (addr, err)) from err
            time.sleep(ES100I2C.ERROR_DELAY_SEC)
            count += 1

    def write(self, data):
        """ write """
        count = 0
        while True:
            try:
                self._smbus.write_byte(self._i2c_address, data)
                return
            except (OSError, IOError) as err:
                if count > 10:
                    raise ES100I2CError('i2c write 0x%02x: %s' % (data, err)) from err
            time.sleep(ES100I2C.ERROR_DELAY_SEC)
            count += 1
