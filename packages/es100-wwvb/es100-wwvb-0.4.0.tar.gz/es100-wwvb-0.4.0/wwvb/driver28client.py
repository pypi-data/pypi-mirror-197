"""

    NTP4 - Shared Memory Driver (#28)
    https://www.ntp.org/documentation/drivers/driver28/

    https://github.com/ntp-project/ntp/blob/master-no-authorname/ntpd/refclock_shm.c

    NTPD uses SysV IPC vs Posix IPC

"""

import os
import sys
import pwd
import grp
import logging
import datetime

# http://semanchuk.com/philip/sysv_ipc/#shared_memory
# https://github.com/osvenskan/sysv_ipc
# pip install sysv_ipc

try:
    import sysv_ipc
except ModuleNotFoundError:
    sysv_ipc = None

# https://github.com/ntp-project/ntp/blob/master-no-authorname/ntpd/refclock_shm.c
NTPD_DEFAULT_KEY = 0x4E545030

# Unclear how to code this up cleanly.
# We can assume that all this code reduces the received clock precision to around -5 or 31.25 milliseconds
NTPD_PRECISION = {
    -10: pow(2, -10),   # 0.9765625 milliseconds
     -9: pow(2, -9),    # 1.953125 milliseconds
     -8: pow(2, -8),    # 3.90625 milliseconds
     -7: pow(2, -7),    # 7.8125 milliseconds
     -6: pow(2, -6),    # 15.625 milliseconds
     -5: pow(2, -5),    # 31.25 milliseconds
     -4: pow(2, -4),    # 62.5 milliseconds
     -3: pow(2, -3),    # 125 milliseconds
     -2: pow(2, -2),    # 250 milliseconds
     -1: pow(2, -1),    # 0.5 seconds
      0: pow(2,  0),    # 1 second
     +1: pow(2, +1),    # 2 seconds
     +2: pow(2, +2),    # 4 seconds
     +3: pow(2, +3),    # 8 seconds
     +4: pow(2, +4),    # 16 seconds
     +5: pow(2, +5),    # 32 seconds
     +5: pow(2, +6),    # 64 seconds
}

class Driver28ClientError(Exception):
    """ raise this any Driver28Client error """

class Driver28Client:
    """ Driver28Client()
    :param unit: The unit number of this clock source (0 thru 255)
    """

    ARCH_TO_BITS = {
        'i386': 32,
        'i686': 32,
        'x86_64': 64,
        'armv6l': 32,
        'armv7l': 32,
        'arm64': 64,
        'arch64': 64,
        'aarch64': 64,
    }

    # 80 = 4(int) * 18 + 4(time_t) * 2
    # for 32 bit machine
    SHM_LAYOUT32 = {
        'mode':                 ( 0, 4, 'int'),         # size 4        # int mode
        'count':                ( 4, 4, 'int'),         # size 4        # volatile int count
        'clockTimeStampSec':    ( 8, 4, 'time_t'),      # size 4        # time_t clockTimeStampSec
        'clockTimeStampUSec':   (12, 4, 'int'),         # size 4        # int clockTimeStampUSec
        'receiveTimeStampSec':  (16, 4, 'time_t'),      # size 4        # time_t receiveTimeStampSec
        'receiveTimeStampUSec': (20, 4, 'int'),         # size 4        # int receiveTimeStampUSec
        'leap':                 (24, 4, 'int'),         # size 4        # int leap
        'precision':            (28, 4, 'int'),         # size 4        # int precision
        'nsamples':             (32, 4, 'int'),         # size 4        # int nsamples
        'valid':                (36, 4, 'int'),         # size 4        # volatile int valid
        'clockTimeStampNSec':   (40, 4, 'unsigned'),    # size 4        # unsigned clockTimeStampNSec
        'receiveTimeStampNSec': (44, 4, 'unsigned'),    # size 4        # unsigned receiveTimeStampNSec
        'dummy':                (48, 32, 'int[8]')      # size 4 * 8    # int[8]
    }

    # 96 = 4(int) * 18 + 8(time_t) * 2 + 4(padding) + 4(padding)
    # for M1 Mac (arm64) or R.Pi arch64
    SHM_LAYOUT64 = {
        'mode':                 ( 0, 4, 'int'),         # size 4        # int mode
        'count':                ( 4, 4, 'int'),         # size 4        # volatile int count
        'clockTimeStampSec':    ( 8, 8, 'time_t'),      # size 8        # time_t clockTimeStampSec
        'clockTimeStampUSec':   (16, 4, 'int'),         # size 4        # int clockTimeStampUSec
        # padding 4
        'receiveTimeStampSec':  (24, 8, 'time_t'),      # size 8        # time_t receiveTimeStampSec
        'receiveTimeStampUSec': (32, 4, 'int'),         # size 4        # int receiveTimeStampUSec
        'leap':                 (36, 4, 'int'),         # size 4        # int leap
        'precision':            (40, 4, 'int'),         # size 4        # int precision
        'nsamples':             (44, 4, 'int'),         # size 4        # int nsamples
        'valid':                (48, 4, 'int'),         # size 4        # volatile int valid
        'clockTimeStampNSec':   (52, 4, 'unsigned'),    # size 4        # unsigned clockTimeStampNSec
        'receiveTimeStampNSec': (56, 4, 'unsigned'),    # size 4        # unsigned receiveTimeStampNSec
        # padding 4
        'dummy':                (64, 32, 'int[8]')      # size 4 * 8    # int[8]
    }

    def __init__(self, unit=0, debug=False, verbose=False):
        """ __init__ """

        self._shm = None

        if not sysv_ipc:
            raise Driver28ClientError('sysv_ipc package not installed - no shared memory access')

        try:
            unit = int(unit)
        except ValueError:
            raise Driver28ClientError('unit invalid')

        if not 0 <= unit < 256:
            raise Driver28ClientError('unit invalid')

        self._log = logging.getLogger(__class__.__name__)
        self._debug = debug
        if self._debug:
            self._log.setLevel(logging.DEBUG)
        self._verbose = verbose
        if self._verbose:
            self._log.setLevel(logging.INFO)

        self._key = NTPD_DEFAULT_KEY + unit
        self._attach()

        self._cpu_word_size = self._find_arch()

        # If we wrote some C code, this could be caculated directly
        # However, in order to run this is pure Python, we do some pretty accurate guessing
        # Actually, we wrote some trivial c code and came up with the 80 & 96 numbers
        # then hardcoded it all in here.
        if self._shm.size == 80 and self._cpu_word_size == 32:
            # 4 byte int's and 8 byte time_t's
            self._mapping = Driver28Client.SHM_LAYOUT32
            self._size = 80
        elif self._shm.size == 96 and self._cpu_word_size == 64:
            # 4 byte int's and 16 byte time_t's plus some padding
            self._mapping = Driver28Client.SHM_LAYOUT64
            self._size = 96
        else:
            self._detach()
            self._shm = None
            raise Driver28ClientError('arch and size mismatch/unknown')

        self._log.info('SHM connected: %r', self)

        # starting thing off by reading the shared memory - we don't do anything with it yet
        self.load()

    def _attach(self):
        """ _attach """
        try:
            self._shm = sysv_ipc.SharedMemory(self._key)
        except Exception as err:
            raise Driver28ClientError('unable to attach to shared memory: %s' % (err)) from err
        self._log.debug('SHM attached')

    def _detach(self):
        """ _attach """
        if self._shm:
            self._shm.detach()
            self._log.debug('SHM detached')
            # self._shm.remove()

    def __del__(self):
        """ __del__ """
        self._detach()
        self._shm = None

    def __str__(self):
        """ __str__ """
        return '0x%08X+%d' % (NTPD_DEFAULT_KEY, self._shm.key - NTPD_DEFAULT_KEY)

    def __repr__(self):
        """ __repr__ """
        try:
            uid = pwd.getpwuid(self._shm.uid).pw_name
        except KeyError:
            uid = str(self._shm.uid)
        try:
            gid = grp.getgrgid(self._shm.gid).gr_name
        except KeyError:
            gid = str(self._shm.gid)
        return '{id:%d, key:0x%08X, size:%d, mode:"%s", uid:"%s", gid:"%s", attached:%s, number_attached:%d}' % (
                    self._shm.id,
                    self._shm.key,
                    self._shm.size,
                    self._decode_mode(self._shm.mode),
                    uid,
                    gid,
                    self._shm.attached,
                    self._shm.number_attached,
                )

    def _decode_mode(self, mode=None):
        """ _decode_mode """
        if mode is None:
            mode = self._shm.mode
        rwx = [
                '---','--x','-w-','-wx',
                'r--','r-x','rw-','rwx'
              ]
        return ''.join([
                        '--',
                        rwx[mode >> 6 & 7],
                        rwx[mode >> 3 & 7],
                        rwx[mode      & 7],
                        ])

    def _find_arch(self):
        """ _find_arch """
        arch = os.uname().machine

        try:
            cpu_word_size = Driver28Client.ARCH_TO_BITS[arch]
        except IndexError:
            # maybe the name gives us a clue?
            if arch[-2:] in ['32','64']:
                cpu_word_size = int(arch[-2:])
            else:
                # we guess
                cpu_word_size = 32
        self._log.info('SHM %dbit word size', cpu_word_size)
        return cpu_word_size

    def read(self, byte_count=0, offset=0):
        """ read()
        :param byte_count: Number of bytes to read
        :param offset: Number of bytes from start of shared memory

        :return: The bytes read
        """
        return self._shm.read(byte_count, offset)

    def write(self, some_bytes, offset=0):
        """ write()
        :param some_bytes: The bytes to write
        :param offset: Number of bytes from start of shared memory

        :return: The number of bytes written
        """
        return self._shm.write(some_bytes, offset)

    def load(self):
        """ load()

        Load up the shared memory into instance
        """
        self._shmTime = bytearray(self.read(self._size, 0))
        self._log.info('SHM loaded')

    def unload(self):
        """ unload()

        Unload the instance copy into shared memory
        """
        self.write(self._shmTime, 0)
        self._log.info('SHM unloaded')

    def dump(self, msg=None):
        """ dump()

        :param msg: an extra debug message

        Provide a pretty printed version of the contents of the shared memory.
        Must call load() before calling dump()
        """

        if self._log.getEffectiveLevel() > logging.DEBUG:
            # short cut
            return

        lines = []
        lines += ['%s' % (self)]

        for name, offset_size_ctype in self._mapping.items():
            offset, size, ctype = offset_size_ctype
            value = self._shmTime[offset:offset+size]
            if ctype == 'int':
                int_val = int.from_bytes(value, 'little', signed=True)
                lines += ['%02d %-24s %2d %-8s = %13d' % (offset, name, size, ctype, int_val)]
            elif ctype == 'unsigned':
                int_val = int.from_bytes(value, 'little', signed=False)
                lines += ['%02d %-24s %2d %-8s = %13d' % (offset, name, size, ctype, int_val)]
            elif ctype == 'time_t':
                int_val = int.from_bytes(value, 'little', signed=False)
                dt = datetime.datetime.utcfromtimestamp(int_val).replace(tzinfo=datetime.timezone.utc)
                lines += ['%02d %-24s %2d %-8s = %13d # %s' % (offset, name, size, ctype, int_val, dt)]
            else:
                b = ','.join([('%02x' % v) for v in value])
                if len(b) > 13:
                    b = b[0:13-3] + '...'
                lines += ['%02d %-24s %2d %-8s = %s' % (offset, name, size, ctype, b)]

        if not msg:
            msg = '%r' % (self)

        self._log.debug('%s %s', msg, '\n\t\t'.join(lines))

    def update(self, received_dt, sys_received_dt, leap_second=None):
        """ update()

        :param received_dt: WWVB received date and time
        :param sys_received_dt: System time when received

        Do the nitty-gritty NTP update via shared memory
        """

        self._log.info('update(%s, %s, %s)', received_dt, sys_received_dt, leap_second)

        wwvb_time = received_dt.timestamp()
        sys_time = sys_received_dt.timestamp()

        self.load()
        self._store_value('mode', 1)            # 1 == operational mode 1

        self._store_value('clockTimeStampSec', int(wwvb_time))
        self._store_value('clockTimeStampUSec', int(1000000 * (wwvb_time%1)))
        self._store_value('clockTimeStampNSec', 0)

        self._store_value('receiveTimeStampSec', int(sys_time))
        self._store_value('receiveTimeStampUSec', int(1000000 * (sys_time%1)))
        self._store_value('receiveTimeStampNSec', 0)

        # values taken from include/ntp.h
        if leap_second is None:
            self._store_value('leap', 0)        # LEAP_NOWARNING
        elif leap_second == 'positive':
            self._store_value('leap', 1)        # LEAP_ADDSECOND
        elif leap_second == 'negative':
            self._store_value('leap', 2)        # LEAP_DELSECOND
        else:
            self._store_value('leap', 3)        # LEAP_NOTINSYNC

        self._store_value('precision', -5)      # 1/32'nd of a second. See NTPD_PRECISION above

        count = self._read_value('count')
        count += 1
        self._store_value('count', count)

        self._store_value('valid', 1) # go!
        self.dump('Sending time to NTP count=%d ' % (count))
        self.unload()

    def _read_value(self, name):
        """ _read_value()

        :param name: Name of shmTime element
        :return: Value from shmTime struct
        """

        try:
            offset, size, ctype = self._mapping[name]
        except IndexError:
            return None

        value = self._shmTime[offset:offset+size]
        if ctype == 'int':
            return int.from_bytes(value, 'little', signed=True)
        if ctype == 'unsigned':
            return int.from_bytes(value, 'little', signed=False)
        if ctype == 'time_t':
            int_val = int.from_bytes(value, 'little', signed=False)
            return datetime.datetime.utcfromtimestamp(int_val).replace(tzinfo=datetime.timezone.utc)
        return value

    def _store_value(self, name, value):
        """ _store_value()

        :param name: Name of shmTime element
        :param value: New value
        """

        try:
            offset, size, ctype = self._mapping[name]
        except IndexError:
            #should not happen
            raise Driver28ClientError('%s: invalid structure element name', name)

        if ctype == 'int':
            b = int(value).to_bytes(size, 'little', signed=True)
        elif ctype in ['unsigned', 'time_t']:
            b = int(value).to_bytes(size, 'little', signed=False)
        else:
            #should not happen - we only write int's, unsigned's, and time_t's
            raise Driver28ClientError('%s: invalid ctype', ctype)

        # copy the bytes into place
        for ii in range(len(b)):
            self._shmTime[offset+ii] = b[ii]
