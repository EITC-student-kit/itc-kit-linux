__author__ = 'Kristo Koert'

import imaplib
import threading
import email
from ITCKit.settings.settings import get_mail_settings
from ITCKit.settings import settings
from ITCKit.db import dbc
from ITCKit.core.datatypes import Mail


class MailHandler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def run(self):
        pass


def get_unread_email():
    mail_settings = get_mail_settings()
    mail_service = imaplib.IMAP4_SSL('outlook.office365.com')
    mail_service.login(mail_settings["username"], mail_settings["password"])
    inbox = mail_service.select("inbox")
    result, data = mail_service.uid("search", None, "UNSEEN")
    if mail_settings["first_time"]:
        settings.update_settings("Mail", "first_time", False)
        dbc.add_mail_uid(data[0].split())
    else:
        new_mail_uids = dbc.get_mail_not_read(data[0].split())
        print("newmail-> ", new_mail_uids)
        mail_notifications = []
        if len(new_mail_uids) != 0:
            print(new_mail_uids)
            for mail_uid in new_mail_uids:
                result, data = mail_service.uid('fetch', mail_uid, "(RFC822)")
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                mail_notifications.append(Mail(email_message["From"]))
        dbc.add_to_db(mail_notifications)
        print(dbc.get_all_notifications())

if __name__ == "__main__":
    get_unread_email()