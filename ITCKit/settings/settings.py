__author__ = 'Kristo Koert'

import json
import os
from os.path import join
import getpass

ROOT_PATH = "/home/" + getpass.getuser()


def update_settings(obj, key, value):
    """Updates the value specified.
    :type obj: str
    :type key: str
    :type value: str | bool
    """
    _json_data = json.load(open(_settings_file_path))
    _json_data[obj][key] = value
    json.dump(_json_data, open(_settings_file_path, "w"), sort_keys=True, indent=4, separators=(',', ': '))


def find_and_set_files():

    def find_file_path(file):
        search_in = ROOT_PATH + "/EITC-kit/"
        for root, dirs, files in os.walk(search_in):
            if file in files:
                path = join(root, file)
                return path

    look_for = ["settingsFile", "main_ical", "user_ical", "itckitdb", "Start_Conky"]
    return find_file_path(look_for[0]), find_file_path(look_for[1]), \
        find_file_path(look_for[2]), find_file_path(look_for[3]), find_file_path(look_for[4])

_settings_file_path, MAIN_ICAL_PATH, USER_ICAL_PATH, EITC_DB_PATH, conky_script = find_and_set_files()


if EITC_DB_PATH == None:
    EITC_DB_PATH = ROOT_PATH + "/EITC-kit/Linux-version/ITCKit/db/itckitdb"
update_settings("Conky", "dbPath", EITC_DB_PATH)
update_settings("Timetable", "dbPath", EITC_DB_PATH)
update_settings("Conky", "scriptPath", conky_script)


def get_time_manager_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["TimeManager"]


def get_timetable_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["Timetable"]


def get_email_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["EMail"]


def get_conky_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["Conky"]


def get_notification_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["Notification"]


def set_user_url(url):
    #ToDo implement set_user_url
    pass


def set_main_url(url):
    #ToDo implement set_main_url
    pass
