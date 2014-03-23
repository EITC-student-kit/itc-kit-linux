__author__ = 'Kristo Koert'

import threading
from ITCKit.settings import settings


class UrlChecker(threading.Thread):

    def __init__(self, instance):
        """
        :type instance: SetIcalUrlWindow
        """
        threading.Thread.__init__(self)
        self.instance = instance

    def run(self):
        self.instance._is_checking_url = True
        url = self.instance.entry.get_text()
        try:
            is_valid_ical_url(url)
            settings.update_settings("Timetable", "user_url", url)
            self.instance.info_label = "URL Verified and saved!"
        except Exception:
            self.instance.info_label = "Unable to verify, or invalid URL."
        self.instance._is_checking_url = False


def is_valid_ical_url(url):
    download_ical(url)


def download_ical(url):
    """Returns ical text from url.
    :rtype: str
    """
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


def load_settings():
    pass