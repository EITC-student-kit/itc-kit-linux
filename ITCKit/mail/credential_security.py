__author__ = 'Kristo Koert'

import keyring
from ITCKit.settings import settings
from threading import Thread


def save_to_keyring(username, password):
    settings.update_settings("EMail", "username", username)
    keyring.set_password("EITC-kit", username, password)


class PasswordManager(Thread):

    def __init__(self):
        super(PasswordManager, self).__init__()

    def run(self):
        print("enter get_password()")
        psw = ''
        try:
            psw = keyring.get_password("EITC-kit", settings.get_email_settings()["username"])
        except Exception as e:
            print("An exception occured")
            print(e)
        print("exit get_password()")
        print("psw = ", psw)
        return psw

    def get_password(self):
        return self.run()