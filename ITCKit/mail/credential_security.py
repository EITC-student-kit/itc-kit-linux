__author__ = 'Kristo Koert'

import keyring
from ITCKit.settings import settings


def save_to_keyring(username, password):
    settings.update_settings("EMail", "username", username)
    keyring.set_password("EITC-kit", username, password)


def get_password():
    return keyring.get_password("EITC-kit", settings.get_email_settings()["username"])
