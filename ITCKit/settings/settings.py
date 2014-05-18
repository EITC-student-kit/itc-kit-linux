__author__ = 'Kristo Koert'

import json
import os
from os.path import join
import getpass

ROOT_PATH = "/home/" + getpass.getuser()


def find_and_set_files():

    def find_file_path(file):
        search_in = ROOT_PATH
        for root, dirs, files in os.walk(search_in):
            if file in files:
                path = join(root, file)
                return path

    look_for = ["settingsFile", "main_ical", "user_ical", "itckitdb", "Start_Conky", "itc_icons", "password_retrieval.py"]
    return find_file_path(look_for[0]), find_file_path(look_for[1]), \
           find_file_path(look_for[2]), find_file_path(look_for[3]), find_file_path(look_for[4]), \
           find_file_path(look_for[5]).replace("itc_icons", "Icon1.png"), find_file_path(look_for[6])

_settings_file_path, MAIN_ICAL_PATH, USER_ICAL_PATH, EITC_DB_PATH, conky_script, icon_path, psw_script_path = find_and_set_files()


def update_settings(obj, key, value):
    """Updates the value specified.
    :type obj: str
    :type key: str
    :type value: str | bool
    """
    _json_data = json.load(open(_settings_file_path))
    _json_data[obj][key] = value
    json.dump(_json_data, open(_settings_file_path, "w"), sort_keys=True, indent=4, separators=(',', ': '))


if EITC_DB_PATH is None:
    EITC_DB_PATH = ROOT_PATH + "/EITC-kit/Linux-version/ITCKit/db/itckitdb"
update_settings("Conky", "dbPath", EITC_DB_PATH)
update_settings("Timetable", "dbPath", EITC_DB_PATH)
update_settings("Conky", "scriptPath", conky_script)
update_settings("Other", "icon_path", icon_path)
update_settings("EMail", "scriptPath", psw_script_path)


def get_time_manager_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_settings_file_path))
    return _json_data["Time manager"]


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


def get_other_settings():
    _json_data = json.load(open(_settings_file_path))
    return _json_data["Other"]
