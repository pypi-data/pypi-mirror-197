""" WWVB 60Khz Full functionality receiver/parser for i2c bus based ES100-MOD

A time and date decoder for the ES100-MOD WWVB receiver.
See README.md for detailed/further reading.

Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
"""

import time
from datetime import datetime, timezone
import logging
from enum import IntEnum
import random

from .gpio_control import ES100GPIO, ES100GPIOError
from .i2c_control import ES100I2C, ES100I2CError

I2C_DEFAULT_BUS = 1
ES100_SLAVE_ADDR = 0x32             # I2C slave address

T_WAKEUP = 0.001                    # Wakeup time - 1ms
T_1MINUTE_FRAME_RECEPTION = 134     # Reeception time 134 seconds
T_TRACKING_RECEPTION = 24.5         # Tracking Reception 24.5 seconds
T_IRQ_DELAY = 0.1                   # -100 thru 100 ms

class ES100Error(Exception):
    """ raise this any ES100 error """

class ES100:
    """ ES100()

    :param antenna: 1 or 2 or None
    :param en: EN pin number
    :param irq: IRQ pin number
    :param bus: i2c bus number
    :param address: i2c address
    :param debug: True to enable debug messages
    :param verbose: True to enable verbose messages
    :return: New instance of ES100GPIO()

    ES100() provides all the controls for communicating with the ES100-MOD receiver
    """

    # ES100-MOD Registers
    class REG(IntEnum):
        """ :meta private: """

        CONTROL0        = 0x00
        CONTROL1        = 0x01
        IRQ_STATUS      = 0x02
        STATUS0         = 0x03
        YEAR            = 0x04
        MONTH           = 0x05
        DAY             = 0x06
        HOUR            = 0x07
        MINUTE          = 0x08
        SECOND          = 0x09
        NEXT_DST_MONTH  = 0x0a
        NEXT_DST_DAY    = 0x0b
        NEXT_DST_HOUR   = 0x0c
        DEVICE_ID       = 0x0d   # should return 0x10 (the device id of ES100)
        RESERVED0       = 0x0e
        RESERVED1       = 0x0f

    # Control0 Read/Write
    class CONTROL0(IntEnum):
        """ :meta private: """
        START           = 0x01  # 1 == start processing, 0 == stops/stopped receiving
        ANT1_OFF        = 0x02  # 1 == Antenna1 disabled, 0 == Antenna1 enabled
        ANT2_OFF        = 0x04  # 1 == Antenna2 disabled, 0 == Antenna2 enabled
        START_ANT       = 0x08  # 1 == Start reception with Antenna2, 0 = Antenna1
        TRACKING_ENABLE = 0x10  # 1 == Tracking mode enabled, 0 == disabled
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

        # Valid values are:
        # 0x01 normal mode, starts on Antenna1, toggles between antennas
        # 0x03 (Antenna 2 only)
        # 0x05 (Antenna 1 Only)
        # 0x09 normal mode, starts on Antenna2, toggles between antennas
        # 0x13 tracking mode, Antenna2
        # 0x15 tracking mode, Antenna1

    # Control1 Read/Write (presently unused)
    class CONTROL1(IntEnum):
        """ :meta private: """
        BIT0            = 0x01
        BIT1            = 0x02
        BIT2            = 0x04
        BIT3            = 0x08
        BIT4            = 0x10
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

    # IRQ Status Read only
    class IRQ_STATUS(IntEnum):
        """ :meta private: """
        RX_COMPLETE     = 0x01 # 1 == Reception complete, 0 == (default)
        BIT1            = 0x02
        CYCLE_COMPLETE  = 0x04 # 1 == Cycle Complete, unsuccessful reception, 0 == (default)
        BIT3            = 0x08
        BIT4            = 0x10
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

    # Status0 Read Only
    class STATUS0(IntEnum):
        """ :meta private: """
        RX_OK           = 0x01  # 1 == successful reception
        ANT             = 0x02  # 1 == Antenna2, 0 == Antenna1
        BIT2            = 0x04
        LSW0            = 0x08  # LSW[0:1] 00 == Current month doesn't have leap second
        LSW1            = 0x10  # LSW[0:1] 10 == Negative leap second, 11 == positive leap second
        DST0            = 0x20  # DST[0:1] 00 == No DST, 10 == DST begins today
        DST1            = 0x40  # DST[0:1] 11 == DST in effect, 01 == DST ends today
        TRACKING        = 0x80  # 1 == reception was tracking operation

    def __init__(self, antenna=None, en=None, irq=None, bus=None, address=None, debug=False, verbose=False):
        """ :meta private: """

        if antenna:
            # user defined
            if antenna not in [1, 2]:
                raise ES100Error('antenna number incorrect: %d' % (antenna))
            self._antenna = antenna
        else:
            # we choose for the userr
            self._antenna = random.choice([1, 2])

        self._log = logging.getLogger(__class__.__name__)
        self._debug = debug
        if self._debug:
            self._log.setLevel(logging.DEBUG)
        self._verbose = verbose
        if self._verbose:
            self._log.setLevel(logging.INFO)

        self._gpio_en = en
        if not self._gpio_en:
            raise ES100Error('gpio en (enable) pin must be provided')

        self._gpio_irq = irq
        if not self._gpio_irq:
            raise ES100Error('gpio irq (interrupt-request) pin must be provided')

        self._i2c_bus = bus
        if self._i2c_bus is not None:
            if self._i2c_bus < 0 or self._i2c_bus > 999:
                raise ES100Error('i2c bus number error: %s' % bus)
        else:
            self._i2c_bus = I2C_DEFAULT_BUS

        self._i2c_address = address
        if self._i2c_address is not None:
            if self._i2c_address < 0 or self._i2c_address > 127:
                raise ES100Error('i2c address number error: %s' % address)
        else:
            self._i2c_address = ES100_SLAVE_ADDR

        # start settting up hardware - if it exists!

        self._gpio = None
        self._i2c = None

        try:
            self._gpio = ES100GPIO(self._gpio_en, self._gpio_irq, debug=debug)
        except ES100GPIOError as err:
            raise ES100Error('GPIO open error: %s' % (err)) from err
        self._log.info('gpio connected (EN/Enable=%d IRQ=%d)', self._gpio_en, self._gpio_irq)

        self._enable()
        time.sleep(T_WAKEUP)

        try:
            self._i2c = ES100I2C(self._i2c_bus, self._i2c_address, debug=debug)
        except ES100I2CError as err:
            raise ES100Error('i2c bus %d open error: %s' % (self._i2c_bus, err)) from err
        self._log.info('i2c connected (bus=%d address=0x%02x)', self._i2c_bus, self._i2c_address)

        self._device_id = None
        self._recv_date = {}
        self._recv_time = {}
        self._recv_dst_info = {}
        self._system_time_received = None
        self._wwvb_time_received = None
        self._delta_seconds = None
        self._status0 = 0x00
        self._irq_status = 0x00
        self._control0 = 0x00
        self._status_ok = 0x00
        self._rx_antenna = None
        self._tracking_operation = None
        self._rx_complete = None
        self._cycle_complete = None
        self._leap_second = None
        self._lsw_bits = 0x0
        self._dst_bits = 0x0
        self._dst = None
        self._dst_begins_today = None
        self._dst_ends_today = None
        self._dst_next = [None, None, None]
        self._dst_special = None

        # find device id
        if not self._es100_device_id():
            raise ES100Error('i2c bus probe failed to find ES100 chip')

    def __del__(self):
        """ __del__ """

        if self._i2c:
            self._i2c = None
            self._log.info('i2c disconnected')

        self._disable()
        time.sleep(T_WAKEUP)

        if self._gpio:
            self._gpio = None
            self._log.info('gpio disconnected')

    def system_time(self):
        """ system_time()

        :return: datetime value for reception system time

        After a successful reception, this returns the time the reception interrupt happened.
        """
        if not self._rx_complete and not self._status_ok:
            raise ES100Error('No reception yet')
        return self._system_time_received

    def wwvb_time(self):
        """ wwvb_time()

        :return: datetime value for WWVB received time

        After a successful reception, this returns the time heard from WWVB
        """
        if not self._rx_complete and not self._status_ok:
            raise ES100Error('No reception yet')
        return self._wwvb_time_received

    def rx_antenna(self):
        """ rx_antenna()

        :return: The antenna number (1 or 2)

        After a successful reception, this returns the antenna used (1 or 2)
        """
        if not self._rx_complete and not self._status_ok:
            raise ES100Error('No reception yet')
        return self._rx_antenna

    def leap_second(self):
        """ leap_second()

        :return: The leap second value returned by WWVB
        """
        if not self._rx_complete and not self._status_ok:
            raise ES100Error('No reception yet')
        return self._leap_second

    def delta_seconds(self):
        """ delta_seconds()

        :return: The delta seconds between the system received time and the wwvb time
        """
        if not self._rx_complete and not self._status_ok:
            raise ES100Error('No reception yet')
        return self._delta_seconds

    def _enable(self):
        """ _enable """
        self._gpio.en_high()
        self._log.info('enable set high')

    def _disable(self):
        """ _disable """
        self._gpio.en_low()
        self._log.info('enable set low')

    def _irq_wait(self):
        """ _irq_wait """
        self._log.info('wait for irq')
        self._gpio.irq_wait()

    def _read_register(self, addr):
        """ _read_register """
        try:
            self._i2c.write(addr)
        except ES100I2CError as err:
            self._log.error('i2c read: %s', err)
            raise ES100Error('i2c read: %s' % (err)) from err

        try:
            rval = self._i2c.read()
        except ES100I2CError as err:
            self._log.error('i2c read: %s', err)
            raise ES100Error('i2c read: %s' % (err)) from err
        self._log.debug('register %d read => 0x%02x', addr, rval & 0xff)
        return rval & 0xff

    def _write_register(self, addr, data):
        """ _write_register """
        self._log.debug('register %d write <= 0x%02x', addr, data)
        try:
            self._i2c.write_addr(addr, data)
        except ES100I2CError as err:
            self._log.error('i2c write: %s', err)
            raise ES100Error('i2c write: %s' % (err)) from err

    def _get_device_id(self):
        """ _get_device_id """
        self._log.debug('get device_id')
        #Read DEVICE_ID register
        return self._read_register(int(ES100.REG.DEVICE_ID))

    def _get_irq_status(self):
        """ _get_irq_status """
        self._log.debug('get irq')
        #Read IRQ status register
        return self._read_register(int(ES100.REG.IRQ_STATUS))

    def _get_status0(self):
        """ _get_status0 """
        self._log.debug('get status0')
        #Read STATUS0 register
        return self._read_register(int(ES100.REG.STATUS0))

    def _get_control0(self):
        """ _get_control0 """
        self._log.debug('get control0')
        #Read CONTROL0 register
        return self._read_register(int(ES100.REG.CONTROL0))

    def _write_control0(self, val):
        """ _write_control0 """
        self._write_register(int(ES100.REG.CONTROL0), val)

    def _report_status0_and_irq_reg(self):
        """ _report_status0_and_irq_reg """
        self._irq_status = self._get_irq_status()
        self._cycle_complete = bool(self._irq_status & ES100.IRQ_STATUS.CYCLE_COMPLETE)
        self._rx_complete = bool(self._irq_status & ES100.IRQ_STATUS.RX_COMPLETE)

        if not self._rx_complete:
            self._log.info('irq_status = 0x%02x <...,%s,-,%s>',
                                self._irq_status,
                                'CYCLE_COMPLETE' if self._cycle_complete else '-',
                                'RX_COMPLETE' if self._rx_complete else '-',
                        )
            return

        # status0 should now contain information
        self._status0 = self._get_status0()
        self._tracking_operation = bool(self._status0 & ES100.STATUS0.TRACKING)
        self._rx_antenna = 'Antenna2' if self._status0 & ES100.STATUS0.ANT else 'Antenna1'
        self._status_ok = bool(self._status0 & ES100.STATUS0.RX_OK)

        self._log.info('irq_status = 0x%02x <...,%s,-,%s> | status0 = 0x%02x <%s,...,%s,%s>',
                            self._irq_status,
                            'CYCLE_COMPLETE' if self._cycle_complete else '-',
                            'RX_COMPLETE' if self._rx_complete else '-',
                            self._status0,
                            'TRACKING' if self._tracking_operation else '-',
                            self._rx_antenna if self._cycle_complete or self._rx_complete else '-',
                            'RX_OK' if self._status_ok else '-',
                    )

    def _report_control0_reg(self):
        """ _report_control0_reg """
        self._control0 = self._get_control0()

        # we don't need to save any of thise bits becuase they aren't referenced
        tracking_enabled = bool(self._control0 & ES100.CONTROL0.TRACKING_ENABLE)
        start_ant =  2 if self._control0 & ES100.CONTROL0.START_ANT else 1
        ant2_off = bool(self._control0 & ES100.CONTROL0.ANT2_OFF)
        ant1_off = bool(self._control0 & ES100.CONTROL0.ANT1_OFF)
        start = bool(self._control0 & ES100.CONTROL0.START)

        self._log.info('control0 = 0x%02x <...,%s,%s,%s,%s,%s>',
                            self._control0,
                            'TRACKING_ENABLE' if tracking_enabled else '-',
                            'Antenna' + str(start_ant),
                            'ANT2_OFF' if ant2_off else '-',
                            'ANT1_OFF' if ant1_off else '-',
                            'START' if start else '-',
                    )

    def _start_rx(self, tracking=False):
        """ _start_rx """
        if not tracking:
            self._log.info('start rx via Antenna%d', self._antenna)
            if self._antenna == 1:
                self._write_control0(ES100.CONTROL0.START)
            else:
                self._write_control0(ES100.CONTROL0.START | ES100.CONTROL0.START_ANT)
        else:
            self._log.info('start tracking via Antenna%d', self._antenna)
            control0 = ES100.CONTROL0.START | ES100.CONTROL0.TRACKING_ENABLE
            if self._antenna == 1:
                control0 |= ES100.CONTROL0.ANT2_OFF
            else:
                control0 |= ES100.CONTROL0.ANT1_OFF
            self._write_control0(control0)
        # perform read of control0 register
        self._report_control0_reg()

    def _start_tracking(self):
        """ _start_tracking """

        # The duration of a tracking reception is ~24.5 seconds (22 seconds of reception,
        # plus ~2.5 seconds of processing and IRQ- generation),

        # The write to Control 0 must occur when the clock second transitions to :55
        # (refer to the timing diagrams to see how this supports drift between +4s and -4s).

        self._wait_till_55seconds()
        self._start_rx(tracking=True)

    @classmethod
    def _bcd(cls, val):
        """ _bcd """
        return (val & 0x0f) + ((val >> 4) & 0x0f) * 10

    def _es100_device_id(self):
        """ _es100_device_id """

        if self._device_id is None:
            try:
                self._device_id = self._get_device_id()
            except ES100Error:
                self._device_id = 0x00

        if self._device_id != 0x10:
            self._log.info('device ID = 0x%02x (unknown device)', self._device_id)
            return False

        self._log.info('device ID = 0x%02x (confirmed as ES100-MOD)', self._device_id)
        return True

    def _wait_till_55seconds(self):
        """ _wait_till_55seconds """

        # Tracking should not start till :55 second point
        # (we assume ntp is running - chicken-n-egg issue)

        time_now = datetime.utcnow()
        remaining_seconds = 55.0 - (time_now.second + time_now.microsecond/1000000.0)
        if remaining_seconds < 0.0:
            remaining_seconds += 60.0
        self._log.debug('sleeping %.1f seconds till :55 point', remaining_seconds)
        # The suspension time may be longer than requested by an arbitrary amount, because
        # of the scheduling of other activity in the system.
        # We ignore this fact presently
        time.sleep(remaining_seconds)

    def _es100_receive(self, tracking=False):
        """ _es100_receive """

        # We should be enabled already
        # self._enable()
        # time.sleep(T_WAKEUP)

        # start reception
        if not tracking:
            self._start_rx()
        else:
            self._start_tracking()

        # loop until time received
        while True:
            self._report_status0_and_irq_reg()

            if self._rx_complete:
                # we have info - let's  go do stuff!
                return

            self._system_time_received = None
            # now we wait - how long? 134 seconds according to the manual
            # we don't actually read the IRQ line
            # we look for an edge (up or down) - way more cpu efficient!
            self._irq_wait()
            # save away the current time quikly - i.e. time of decoded reception
            self._system_time_received = datetime.utcnow().replace(tzinfo=timezone.utc)
            # round down to milliseconds
            # WWVB is accurate; but our reception isn't down to the microsecond ('cause linux)
            msec = int(self._system_time_received.microsecond/1000.0)
            self._system_time_received = self._system_time_received.replace(microsecond=msec*1000)

            # We don't assume that the interrupt has compeleted; we loop around and recheck

        # yippe - there should be a reception (or tracking)

    def time(self, antenna=None, tracking=False):
        """ time()

        :param antenna: Select antenna (None, 1, or 2)
        :param tracking: False means receive operation, True means tracking operation
        :return: datetime value for reception system time

        After a successful reception, this returns the time heard from WWVB
        """

        if antenna:
            # user defined
            if antenna not in [1, 2]:
                raise ES100Error('antenna number incorrect: %d' % (antenna))
            self._antenna = antenna
        else:
            # swap 2 -> 1 and 1 -> 2
            self._antenna = 2 if self._antenna == 1 else 1

        try:
            # receive time from WWVB
            self._es100_receive(tracking)
        except ES100Error as err:
            self._log.warning('read/receive failed: %s', err)
            return None

        if self._tracking_operation:
            if not self._status_ok:
                self._log.debug('tracking operation unsuccessful, %s', self._rx_antenna)
                return None

            # No value for date/time or other items in tracking mode; just second.
            # Manual says:
            # Tracking detects the WWVB sync word, including the leading “0” at second :59,
            # and provides (in register 0x09) the current WWVB second that begins on the
            # falling-edge of IRQ-.
            # Note that the registers representing the Year, Month, Day, Hour, Minute
            # and Next DST are not valid for a tracking reception.

            self._recv_date = {}
            self._recv_time = {}
            self._recv_dst_info = {}

            for reg in [ES100.REG.SECOND]:
                self._recv_time[reg.name] = self._read_register(int(reg.value))

            seconds = ES100._bcd(self._recv_time['SECOND'] & 0x7f)
            self._log.info('tracking operation successful, %02d at system time %02d.%03d, %s',
                                seconds,
                                self._system_time_received.second,
                                int(self._system_time_received.microsecond / 1000),
                                self._rx_antenna
                            )

            # we return an obviously wrong result. Only the second value is correct.
            self._wwvb_time_received = datetime(
                                    1, 1, 1,
                                    0, 0, seconds,
                                    microsecond=0,
                                    tzinfo=timezone.utc
                            )

            return self._wwvb_time_received

        if not self._status_ok:
            self._log.debug('reception unsuccessful, %s', self._rx_antenna)
            # No value for data/time, didn't get reception
            return None

        # read all the date, time, and dst registers
        self._recv_date = {}
        self._recv_time = {}
        self._recv_dst_info = {}
        for reg in [ES100.REG.YEAR, ES100.REG.MONTH, ES100.REG.DAY]:
            self._recv_date[reg.name] = self._read_register(int(reg.value))
        for reg in [ES100.REG.HOUR, ES100.REG.MINUTE, ES100.REG.SECOND]:
            self._recv_time[reg.name] = self._read_register(int(reg.value))
        for reg in [ES100.REG.NEXT_DST_MONTH, ES100.REG.NEXT_DST_DAY, ES100.REG.NEXT_DST_HOUR]:
            self._recv_dst_info[reg.name] = self._read_register(int(reg.value))
        self._log.debug('recv date = %s, recv time = %s, dst_info = %s',
                            self._recv_date,
                            self._recv_time,
                            self._recv_dst_info
                        )

        # leap second and DST information is coded in two 2-bit areas
        # while this looks like a perdantic way to code this up; it's easy to understand
        self._lsw_bits = (0x2 if self._status0 & ES100.STATUS0.LSW1 else 0x0) | (0x1 if self._status0 & ES100.STATUS0.LSW0 else 0x0)
        self._dst_bits = (0x2 if self._status0 & ES100.STATUS0.DST1 else 0x0) | (0x1 if self._status0 & ES100.STATUS0.DST0 else 0x0)

        if self._lsw_bits == 0x0 or self._lsw_bits == 0x01:
            self._leap_second = None
        if self._lsw_bits == 0x2:
            self._leap_second = 'negative'
            self._log.info('%s leap second', self._leap_second)
        elif self._lsw_bits == 0x3:
            self._leap_second = 'positive'
            self._log.info('%s leap second', self._leap_second)

        if self._dst_bits == 0x0:
            self._dst = self._dst_begins_today = self._dst_ends_today = False
        elif self._dst_bits == 0x1:
            self._dst = self._dst_ends_today = True
            self._dst_begins_today = False
        elif self._dst_bits == 0x2:
            self._dst = self._dst_ends_today = False
            self._dst_begins_today = True
        elif self._dst_bits == 0x3:
            self._dst = True
            self._dst_begins_today = self._dst_ends_today = False

        if self._dst or self._dst_begins_today or self._dst_ends_today:
            self._log.info('DST info: %s %s %s',
                                'DST' if self._dst else '',
                                'BEGINS-TODAY' if self._dst_begins_today else '',
                                'ENDS-TODAY' if self._dst_ends_today else '',
                            )

        # Next DST transition info
        self._dst_next = [
                            ES100._bcd(self._recv_dst_info['NEXT_DST_MONTH'] & 0x1f),
                            ES100._bcd(self._recv_dst_info['NEXT_DST_DAY'] & 0x3f),
                            ES100._bcd(self._recv_dst_info['NEXT_DST_HOUR'] & 0x0f),
                        ]
        dst_special = self._recv_dst_info['NEXT_DST_HOUR'] & 0xf0 >> 4
        if dst_special & 0x80 == 0x00:
            self._dst_special = ''      # No DST Special condition
        elif dst_special & 0x07 == 0x00:
            self._dst_special = 'DST date and time is outside of defined schedule table'
        elif dst_special & 0x07 == 0x01:
            self._dst_special = 'DST off (regardless of date)'
        elif dst_special & 0x07 == 0x02:
            self._dst_special = 'DST on (regardless of date)'
        else:
            self._dst_special = None # invalid

        self._log.info('Next DST transition YYYY:%02d:%02d @ %02d:00:00 %s',
                            self._dst_next[0], self._dst_next[1], self._dst_next[2],
                            self._dst_special
                        )

        self._wwvb_time_received = datetime(
                                ES100._bcd(self._recv_date['YEAR'] & 0xff) + 2000,
                                ES100._bcd(self._recv_date['MONTH'] & 0x1f),
                                ES100._bcd(self._recv_date['DAY'] & 0x3f),
                                ES100._bcd(self._recv_time['HOUR'] & 0x3f),
                                ES100._bcd(self._recv_time['MINUTE'] & 0x7f),
                                ES100._bcd(self._recv_time['SECOND'] & 0x7f),
                                microsecond=0,
                                tzinfo=timezone.utc
                        )

        # Success! We have date and time!
        self._delta_seconds = (self._system_time_received - self._wwvb_time_received).total_seconds()
        self._log.info('Reception of %s at system time %s with difference %.3f via %s',
                                self._wwvb_time_received,
                                self._system_time_received,
                                self._delta_seconds,
                                self._rx_antenna
                        )

        # self._disable()
        # time.sleep(T_WAKEUP)

        return self._wwvb_time_received
