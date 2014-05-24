__author__ = 'Kristo Koert'

import threading
import email
import time
import subprocess
from imaplib import IMAP4_SSL
from itc_kit.settings.settings import get_email_settings
from itc_kit.settings import settings
from itc_kit.db import dbc
from itc_kit.core.datatypes import EMail
from os import getenv


class MailHandler(threading.Thread):
    """
    This class deals with checking for new unread email at outlook.office365.com.

    This class is a thread that is run on activation of the app that waits idly until the EMail objects value activated
     is set to true in the ical setting file. After this has happened it will try to connect to a account
    """
    connection = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.mail_settings = get_email_settings()

    def run(self):
        while True:
            if self.mail_settings["activated"]:
                self.get_unread_email()
            else:
                time.sleep(1)

    def connect_to_account(self):
        try:
            mail_service = IMAP4_SSL('outlook.office365.com')
            cmd = "python3 " + getenv("HOME") + "/.itc-kit/password_retrieval.py"
            out = subprocess.check_output(args=cmd, shell=True)
            psw = out.decode()
            mail_service.login(self.mail_settings["username"], psw)
            mail_service.select('INBOX')
            return mail_service
        except Exception as e:
            #print("Exception: ", e, " in connect_to_account()")
            return None

    def get_unread_email(self):
        mail_service = self.connection
        if mail_service is None:
            self.connection = self.connect_to_account()
            time.sleep(1)
        else:
            print("Mail service is not none ->", mail_service)
            result, data = mail_service.uid("search", None, "UNSEEN")
            if self.mail_settings["first_time"]:
                settings.update_settings("EMail", "first_time", False)
                dbc.add_mail_uid(data[0].split())
            else:
                new_mail_uids = dbc.get_mail_not_read(data[0].split())
                mail_notifications = []
                if len(new_mail_uids) != 0:
                    for mail_uid in new_mail_uids:
                        result, data = mail_service.uid('fetch', mail_uid, "(RFC822)")
                        raw_email = data[0][1]
                        #print("Raw email is:", type(raw_email))
                        email_message = email.message_from_bytes(raw_email)
                        mail_notifications.append(EMail(email_message["From"]))
                    #print("nr of notifications added:", len(mail_notifications))
                    dbc.add_to_db(mail_notifications)
