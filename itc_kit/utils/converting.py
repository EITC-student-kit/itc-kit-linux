__author__ = 'Kristo Koert'

from datetime import datetime


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
    from sqlite3 import Timestamp
    ical_dt = ical_dt[ical_dt.find(':') + 1:].replace("T", "")
    return Timestamp(int(ical_dt[:4]), int(ical_dt[4:6]), int(ical_dt[6:8]), int(ical_dt[8:10]) + 3, int(ical_dt[10:12]))


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

if __name__ == "__main__":
    pass
