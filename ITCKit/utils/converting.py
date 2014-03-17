__author__ = 'Kristo Koert'


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
    return Timestamp(int(ical_dt[:4]), int(ical_dt[4:6]), int(ical_dt[6:8]), int(ical_dt[8:10]) + 2, int(ical_dt[10:11]))


def to_list(some_val):
    """:rtype: list"""
    if type(some_val) is not list:
        return list(some_val)
    else:
        return some_val


if __name__ == "__main__":
    pass