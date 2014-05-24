__author__ = 'Kristo Koert'

import json
from os import getenv

SETTINGS_FILE_PATH = getenv("HOME") + '/.itc-kit/settings'


def update_settings(obj, key, value):
    """Updates the value specified.
    :type obj: str
    :type key: str
    :type value: str | bool
    """
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    _json_data[obj][key] = value
    json.dump(_json_data, open(SETTINGS_FILE_PATH, "w"), sort_keys=True, indent=4, separators=(',', ': '))


def get_time_manager_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["Time manager"]


def get_timetable_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["Timetable"]


def get_email_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["EMail"]


def get_conky_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["Conky"]


def get_notification_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["Notification"]


def get_other_settings():
    """:rtype: dict"""
    _json_data = json.load(open(SETTINGS_FILE_PATH))
    return _json_data["Other"]
