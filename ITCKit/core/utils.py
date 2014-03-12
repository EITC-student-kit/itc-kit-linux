__author__ = 'Kristo Koert'


def seconds_to_min(s):
    """Turns seconds input into a time format

    :param s: seconds
    :type s: int
    :returns: formatted string
    """
    h = m = 0
    while s > 60:
        s -= 60
        m += 1
    while m > 60:
        m -= 60
        h += 1
    return "{0:02}:{1:02}:{2:02}".format(h, m, s)


def string_till_symbol(a_string, symbol):
    """Returns the part of the string till next occurrence of break_char, if not present, returns whole string.
        :type a_string: str
        :type a_string: str
    """
    indx = 0
    while indx + len(symbol) < len(a_string):
        if a_string[indx:indx + len(symbol)] == symbol:
            return a_string[:indx]
        else:
            indx += 1
    return a_string


def ical_datetime_to_timestamp(ical_dt):
    """
        :param ical_dt: i.e. "20140508T143000Z"
    """
    from sqlite3 import Timestamp
    return Timestamp(int(ical_dt[:4]), int(ical_dt[4:6]), int(ical_dt[6:8]), int(ical_dt[9:11]) + 2, int(ical_dt[11:13]))


if __name__ == "__main__":
    pass