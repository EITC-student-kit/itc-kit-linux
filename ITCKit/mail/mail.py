__author__ = 'Kristo Koert'

import imaplib

from ITCKit.settings.settings import get_mail_settings


def get_unread_email():
    try:
        #ToDo finish implementing get_unread_email
        settings = get_mail_settings()
        mail_service = imaplib.IMAP4_SSL('outlook.office365.com')
        #Deal with invalid username and password
        mail_service.login(settings["username"], settings["password"])
        inbox = mail_service.select("inbox")
        result, data = mail_service.search(None, '(UNSEEN SENTSINCE {0})'.format(get_mail_activation_date()))
        ids = data[0]
        id_list = ids.split()
        print(len(id_list))
        latest_email_id = id_list[-1]
        print(id_list[-1])
        # message body> RFC822
        result, data = mail_service.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
    except:
        print("Handle")
    finally:
        return raw_email


if __name__ == "__main__":
    print(get_unread_email())