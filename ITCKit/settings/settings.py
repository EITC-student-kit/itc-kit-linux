__author__ = 'Kristo Koert'

#ToDo implement settings system via writing to file

import json
import os

#/home/kristo/Programming/ITCKit/ITCKit/settings/db/itckitdb
#/home/kristo/Programming/ITCKit/ITCKit/db/itckitdb
_json_data = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/settingsFile"))

#Time Manager Settings

_time_manager_active = _json_data["TimeManager"]["activated"]

#Timetable Settings

_timetable_activated = _json_data["Timetable"]["activated"]
_user_url = _json_data["Timetable"]["user_url"]
_main_url = _json_data["Timetable"]["main_url"]
_automatic_update = _json_data["Timetable"]["automatic_update"]

#Mail settings

_mail_activated = _json_data["Mail"]["activated"]
_mail_activation_date = _json_data["Mail"]["activated_date"]
_mail_user_name = _json_data["Mail"]["user_name"]
_mail_user_password = _json_data["Mail"]["password"]


#Conky settings

_conky_activated = _json_data["Conky"]["activated"]
_conky_color = _json_data["Conky"]["color"]

#Notification settings

_notification_activated = _json_data["Notification"]["activated"]


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


def get_mail_activation_date():
    global _mail_activation_date
    return _mail_activation_date