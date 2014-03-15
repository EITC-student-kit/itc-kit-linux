__author__ = 'Kristo Koert'


def download_ical(url):
    """Returns ical text from url."""
    import urllib.request
    req = urllib.request.urlopen(url)
    return req.read().decode(encoding='UTF-8')


def string_from_till(a_string, first_symbol, second_symbol):
    """Returns the part of the string till next occurrence of symbol, if not present, returns whole string."""
    a_string = a_string[a_string.find(first_symbol):]
    indx = 0
    while indx + len(second_symbol) < len(a_string):
        if a_string[indx:indx + len(second_symbol)] == second_symbol:
            return a_string[:indx]
        else:
            indx += 1
    return a_string