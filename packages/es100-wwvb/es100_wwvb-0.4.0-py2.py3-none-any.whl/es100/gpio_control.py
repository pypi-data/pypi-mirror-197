""" GPIO control (for EN & IRQ lines)

Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
"""

import sys

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    GPIO = None

IRQ_WAKEUP_DELAY = 10     # 10 second in milliseconds

class ES100GPIOError(Exception):
    """ ES100GPIOError

    ES100GPIOError is raised should errors occur when using ES100GPIO() class.
    """

class ES100GPIO:
    """ ES100GPIO

    :param en: EN pin number
    :param irq: IRQ pin number
    :param debug: True to enable debug messages
    :return: New instance of ES100GPIO()

    All GPIO control is via ES100GPIO() class.
    """

    def __init__(self, en, irq, debug=False):
        """ """
        if not GPIO:
            raise ES100GPIOError('RPi.GPIO package not installed - are you on a Raspberry Pi?')
        self._gpio_en = en
        self._gpio_irq = irq
        self._debug = debug
        self._setup()

    def _setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._gpio_en, GPIO.OUT)
        GPIO.setup(self._gpio_irq, GPIO.IN, GPIO.PUD_DOWN)

    def __del__(self):
        """ __del__ """
        if not GPIO:
            return
        self._close()

    def _close(self):
        """ _close """
        self.en_low()
        GPIO.cleanup()

    def en_low(self):
        """ en_low()

        EN set low
        """
        # Enable Input. When low, the ES100 powers down all circuitry.
        GPIO.output(self._gpio_en, GPIO.LOW)

    def en_high(self):
        """ en_high()

        EN set high
        """
        # Enable Input. When high, the device is operational.
        GPIO.output(self._gpio_en, GPIO.HIGH)

    def irq_wait(self, timeout=None):
        """ irq_wait(self, timeout=None)

        :param timeout: Either None or the number of seconds to control timeout
        :return: True if IRQ/Interrupt is active low, False with timeout

        IRQ- will go active low once the receiver has some info to return.
        """
        # IRQ/Interrupt is active low to signal data available
        if self._debug:
            sys.stderr.write('IRQ WAIT: ')
            sys.stderr.flush()
        while GPIO.input(self._gpio_irq):
            if self._debug:
                sys.stderr.write('H')
                sys.stderr.flush()
            # now wait (for any transition) - way better than looping, sleeping, and checking
            if timeout:
                channel = GPIO.wait_for_edge(self._gpio_irq, GPIO.BOTH, timeout=min(int(timeout*1000), IRQ_WAKEUP_DELAY*1000))
            else:
                channel = GPIO.wait_for_edge(self._gpio_irq, GPIO.BOTH, timeout=IRQ_WAKEUP_DELAY*1000)
            if channel is None:
                # timeout happened
                if self._debug:
                    sys.stderr.write('.')
                    sys.stderr.flush()
                if timeout:
                    timeout -= IRQ_WAKEUP_DELAY
                    if timeout <= 0:
                        if self._debug:
                            sys.stderr.write(' T\n')
                            sys.stderr.flush()
                        return False
        if self._debug:
            sys.stderr.write(' L\n')
            sys.stderr.flush()
        return True
