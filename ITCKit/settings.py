__author__ = 'Kristo Koert'


DATABASE_NAME = "itckitdb"
_user_url = "https://itcollege.ois.ee/en/timetable/ical?student_id=3117&key=34c0482c0c579f1a7da0ea0ba6bda3077d356da8"
_main_url = "https://itcollege.ois.ee/en/timetable/ical?curriculum_id=2&key=01d8d5cbdbb9881fbf103f61c36955e731531a28"


def get_user_url():
    global _user_url
    return _user_url


def get_main_url():
    global _main_url
    return _main_url


def set_user_url(url):
    global _user_url
    _user_url = url
    #ToDo update db


def set_main_url(url):
    global _main_url
    _main_url = url
    #ToDo update db