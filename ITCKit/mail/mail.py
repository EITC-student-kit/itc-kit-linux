__author__ = 'Kristo Koert'

import imaplib

from ITCKit.settings import get_mail_username, get_mail_password


#GDBUS?
#Incoming IMAP Server address imap-mail.outlook.com
mail_service = imaplib.IMAP4_SSL('imap.gmail.com')

mail_service.login(get_mail_username(), get_mail_password())

#list on "folders"ls
mail_service.list()

#interested in inbox
mail_service.select("inbox")

#get all data
result, data = mail_service.search(None, "ALL")

# id-s of data
ids = data[0]

#id-s is a space separated string
id_list = ids.split()

#latest emails id
latest_email_id = id_list[-1]

#"(RFC822)" -> email body
result, data = mail_service.fetch(latest_email_id, "(RFC822)")

#Raw text
raw_email = data[0][1]
print(raw_email)