#!/usr/bin/python3

__author__ = 'Kristo Koert'

from ITCKit.gui import toolbarindicator
from ITCKit.mail import email_system
from ITCKit.core import notification_system
from ITCKit.settings import settings
from gi.repository import Gtk, Gdk
from ITCKit.conky.conky import Conky

if __name__ == "__main__":

    settings.find_and_set_files()

    Gdk.threads_init()
    indicator = toolbarindicator.activate_toolbar()

    Gdk.threads_leave()
    conky_thread = Conky()
    conky_thread.start()
    Gdk.threads_enter()

    Gdk.threads_leave()
    email_thread = email_system.MailHandler()
    email_thread.start()
    Gdk.threads_enter()

    Gdk.threads_leave()
    notification_thread = notification_system.NotificationHandler(indicator, indicator.main_menu)
    notification_thread.start()
    Gdk.threads_enter()

    Gtk.main()
