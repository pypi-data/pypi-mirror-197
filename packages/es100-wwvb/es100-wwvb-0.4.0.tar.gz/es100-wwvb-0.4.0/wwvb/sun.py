""" sun.py

Provide sun tracking functions for CLI wwvb command

Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
"""

import datetime
from math import degrees

import ephem

class Sun:
    """ Sun
    Sun tracking code for sunset/sunrise math.
    Used to decide if a location is in nightime or not.

    All times are kept in UTC.

    Based on PyEphem (which is a fantastic package!)
    https://rhodesmill.org/pyephem/
    """

    def __init__(self, lat, lon, elev=0.0):
        """ __init__ """

        self._sun = ephem.Sun()
        self._viewer = ephem.Observer()
        self._viewer.date = datetime.datetime.utcnow()
        self._viewer.lat = str(lat)
        self._viewer.lon = str(lon)
        self._viewer.elev = elev
        self._viewer.horizon = '0'

    def altitude(self, dtime=None):
        """ altitude """
        if dtime:
            self._viewer.date = dtime
        else:
            self._viewer.date = datetime.datetime.utcnow()
        # always (re)compute as time tends to march-on.
        self._sun.compute(self._viewer)
        # yes, humans prefer degrees
        return degrees(self._sun.alt)

    # look for twilight, which is 6, 12, or 18 degrees below horizon
    # see https://www.weather.gov/lmk/twilight-types

    def civil_twilight(self, dtime=None):
        """ civil_twilight """
        return bool(self.altitude(dtime) <= -6.0)

    def nautical_twilight(self, dtime=None):
        """ nautical_twilight """
        return bool(self.altitude(dtime) <= -12.0)

    def astronomical_twilight(self, dtime=None):
        """ astronomical_twilight """
        return bool(self.altitude(dtime) <= -18.0)
