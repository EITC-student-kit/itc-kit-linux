__author__ = 'Kristo Koert'

import keyring
from itc_kit.settings import settings


def save_to_keyring(username, password):
    """
    Sets the username and password in the keyring that the keyring module deems appropriate.
    """
    settings.update_settings("EMail", "username", username)
    keyring.set_password("EITC-kit", username, password)
