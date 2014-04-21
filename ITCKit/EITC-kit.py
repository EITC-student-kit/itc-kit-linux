__author__ = 'Kristo Koert'

from gui import toolbarindicator
from mail import email_system
from core import notification_system
from gi.repository import Gtk, Gdk
import queue

if __name__ == "__main__":
    #ToDo experimental queue?
    q = queue.Queue()

    Gdk.threads_init()
    indicator = toolbarindicator.activate_toolbar()

    q.put(indicator)

    Gdk.threads_leave()
    email_thread = email_system.MailHandler()
    email_thread.start()
    Gdk.threads_enter()

    q.put(email_thread)

    Gdk.threads_leave()
    notification_thread = notification_system.NotificationHandler(indicator, indicator.main_menu)
    notification_thread.start()
    Gdk.threads_enter()

    q.put(notification_thread)

    q.put(Gtk.main())
