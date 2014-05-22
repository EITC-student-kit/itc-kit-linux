__author__ = 'Kristo Koert'

import json
import os
from os.path import join
import getpass

ROOT_PATH = "/home/" + getpass.getuser() + '/EITC-kit'


def find_file_path(file):
        search_in = ROOT_PATH
        for root, dirs, files in os.walk(search_in):
            if file in files:
                path = join(root, file)
                return path

_SETTINGS_FILE_PATH = find_file_path("settingsFile")


def find_and_set_files():
    main_ical_path = ''
    user_ical_path = ''
    db_path = ''
    conky_script = ''
    icon_path = ''
    psw_script_path = ''

    to_find = {'main_ical': main_ical_path,
               'user_ical': user_ical_path,
               'itckitdb': db_path,
               'Start_Conky': conky_script,
               'itc_icons': icon_path,
               'password_retrieval.py': psw_script_path}

    for file_name in to_find.keys():
        to_find[file_name] = find_file_path(file_name)


    if db_path == '':
        db_path = ROOT_PATH + "/EITC-kit/Linux-version/ITCKit/db/itckitdb"
    update_settings("Conky", "dbPath", to_find['itckitdb'])
    update_settings("Timetable", "dbPath", to_find['itckitdb'])
    update_settings("Conky", "scriptPath", to_find['Start_Conky'])
    update_settings("Other", "icon_path", to_find['itc_icons'].replace('itc_icons', 'Icon3.png'))
    update_settings("EMail", "scriptPath", to_find['password_retrieval.py'])


def update_settings(obj, key, value):
    """Updates the value specified.
    :type obj: str
    :type key: str
    :type value: str | bool
    """
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    _json_data[obj][key] = value
    json.dump(_json_data, open(_SETTINGS_FILE_PATH, "w"), sort_keys=True, indent=4, separators=(',', ': '))


def get_time_manager_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["Time manager"]


def get_timetable_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["Timetable"]


def get_email_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["EMail"]


def get_conky_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["Conky"]


def get_notification_settings():
    """:rtype: dict"""
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["Notification"]


def get_other_settings():
    _json_data = json.load(open(_SETTINGS_FILE_PATH))
    return _json_data["Other"]
