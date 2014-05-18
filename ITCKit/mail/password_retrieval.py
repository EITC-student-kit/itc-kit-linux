__author__ = 'Kristo Koert'

import keyring
from ITCKit.settings import settings


print(keyring.get_password("EITC-kit", settings.get_email_settings()["username"]))
