__author__ = 'Kristo Koert'

import keyring
from ITCKit.settings import settings


def save_to_keyring(username, password):
    print(1)
    settings.update_settings("EMail", "username", username)
    keyring.set_password("EITC-kit", username, password)
    print(2)


def get_password():
    try:
        return keyring.get_password("EITC-kit", settings.get_email_settings()["username"])
    except Exception as e:
        print("Some stuff", e)
        assert False
        return keyring.get_password("EITC-kit", settings.get_email_settings()["username"])
