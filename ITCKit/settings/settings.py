__author__ = 'Kristo Koert'

#ToDo implement settings system via writing to file

import json
import os

_json_data = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/settingsFile"))


def get_time_manager_settings():
    """:rtype: dict"""
    return _json_data["TimeManager"]


def get_timetable_settings():
    """:rtype: dict"""
    return _json_data["Timetable"]


def get_mail_settings():
    """:rtype: dict"""
    return _json_data["Mail"]


def get_conky_settings():
    """:rtype: dict"""
    return _json_data["Conky"]


def get_notification_settings():
    """:rtype: dict"""
    return _json_data["Notifications"]


def set_user_url(url):
    #ToDo implement set_user_url
    pass


def set_main_url(url):
    #ToDo implement set_main_url
    pass
