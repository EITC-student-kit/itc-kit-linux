__author__ = 'Kristo Koert'

#ToDo implement settings system via writing to file

import json
import os

_settings_file_path = os.path.dirname(os.path.abspath(__file__)) + "/settingsFile"

_json_data = json.load(open(_settings_file_path))


def get_time_manager_settings():
    """:rtype: dict"""
    return _json_data["TimeManager"]


def get_timetable_settings():
    """:rtype: dict"""
    return _json_data["Timetable"]


def get_email_settings():
    """:rtype: dict"""
    return _json_data["EMail"]


def get_conky_settings():
    """:rtype: dict"""
    return _json_data["Conky"]


def get_notification_settings():
    """:rtype: dict"""
    return _json_data["Notification"]


def update_settings(obj, key, value):
    """Updates the value specified.
    :type obj: str
    :type key: str
    :type value: str | bool
    """
    _json_data[obj][key] = value
    json.dump(_json_data, open(_settings_file_path, "w"), sort_keys=True, indent=4, separators=(',', ': '))


def set_user_url(url):
    #ToDo implement set_user_url
    pass


def set_main_url(url):
    #ToDo implement set_main_url
    pass
