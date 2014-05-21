__author__ = 'Kristo Koert'

import keyring
from itc_kit.settings import settings

print(keyring.get_password("EITC-kit", settings.get_email_settings()["username"]))
