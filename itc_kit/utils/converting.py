__author__ = 'Kristo Koert'

from datetime import datetime
from datetime import tzinfo, timedelta
from sqlite3 import Timestamp


class EstonianTimezone(tzinfo):
    """
    Changes utc timestamp to Estonian time.
    """
    ZERO = timedelta(hours=0)
    ONE = timedelta(hours=1)
    TWO = timedelta(hours=2)

    def __init__(self):
        tzinfo.__init__(self)

    def utcoffset(self, dt):
        return self.TWO + self.dst(dt)

    def dst(self, dt):
        dston = datetime(datetime.now().year, 3, 30, 1)
        dstoff = datetime(datetime.now().year, 10, 26, 1)
        if dston <= dt.replace(tzinfo=None) < dstoff:
            return self.ONE
        else:
            return self.ZERO

    def tzname(self, dt):
        return "Est/tln"


def sec_to_time(s):
    """:rtype str"""
    h = m = 0
    while s >= 60:
        s -= 60
        m += 1
    while m >= 60:
        m -= 60
        h += 1
    return "{0:02}:{1:02}:{2:02}".format(h, m, s)


def ical_datetime_to_timestamp(ical_dt):
    """
    :param ical_dt: i.e. "20140508T143000Z"
    :rtype Timestamp
    """
    ical_dt = ical_dt[ical_dt.find(':') + 1:].replace("T", "")
    utc_time = Timestamp(int(ical_dt[:4]), int(ical_dt[4:6]), int(ical_dt[6:8]), int(ical_dt[8:10]), int(ical_dt[10:12]))
    diff = get_timezone_difference(utc_time)
    return Timestamp(int(ical_dt[:4]), int(ical_dt[4:6]), int(ical_dt[6:8]), int(ical_dt[8:10]) + diff, int(ical_dt[10:12]))


def to_list(some_val):
    """:rtype: list"""
    if type(some_val) is not list:
        return list(some_val)
    else:
        return some_val


def str_to_datetime(datetime_str):
    """2014-03-24 10:51"""
    return datetime(int(datetime_str[:4]), int(datetime_str[5:7]), int(datetime_str[8:10]),
                    int(datetime_str[11:13]), int(datetime_str[14:16]))


def get_timezone_difference(datetime):
    est_tz = EstonianTimezone()
    est_dt = datetime.replace(tzinfo=est_tz)
    return int(str(est_dt)[21:22])


