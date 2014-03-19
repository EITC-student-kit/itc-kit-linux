__author__ = 'Kristo Koert'

import os

DATABASE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/db/itckitdb"
_user_url = "https://itcollege.ois.ee/en/timetable/ical?student_id=3117&key=34c0482c0c579f1a7da0ea0ba6bda3077d356da8"
_main_url = "https://itcollege.ois.ee/en/timetable/ical?curriculum_id=2&key=01d8d5cbdbb9881fbf103f61c36955e731531a28"
_mail_user_name = "kristo.koert@gmail.com"
_mail_user_password = "password"


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


def get_mail_username():
    global _mail_user_name
    return _mail_user_name


def get_mail_password():
    global _mail_user_password
    return _mail_user_password