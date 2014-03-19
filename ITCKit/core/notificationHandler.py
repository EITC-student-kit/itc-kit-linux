__author__ = 'Kristo Koert'

#ToDo Port to Python 3
from threading import Thread
from time import sleep

from gi.repository import AppIndicator3 as AppIndicator

from ITCKit.db import dbc


class NotificationHandler(Thread):
    """Handles checking if there are any notifications in a database that are due and raises an alarm if they are."""

    _notifications = []

    def __init__(self, indicator, menu_item):
        """Initialization uses the super class Thread __init__ function and sets an Indicator object to be used as
        the place where a notification is raised, if needed. More info on the notification will be displayed on the
        menu_item.

        :param indicator: channel for displaying the notification
        :type indicator: ToolbarIndicator
        :param menu_item: Place to display more notification information
        :type menu_item: gtk.ImageMenuItem
        """
        super(NotificationHandler, self).__init__()
        self._indicator = indicator
        self._get_notifications()
        self._menu_item = menu_item

    def run(self):
        """When thread is started, an endless loop ensues. Constantly checking if any notifications should be raised."""
        while True:
            self._check_notifications()
            sleep(10)

    def _check_notifications(self):
        """Checks if any notifications should be triggered."""
        if self._notifications[0] is not None:
            for notif in self._notifications:
                if notif.is_due():
                    self._raise_notification(notif)
                    self._notifications.remove(notif)

    def _get_notifications(self):
        """Gets notifications from database"""
        self._notifications = dbc.get_all_notifications()

    def _raise_notification(self, notif):
        """Raises notification in Indicator passed as __init__ parameter.

        param: notif: A notification
        type: notif: Notification
        """
        self._indicator.set_status(AppIndicator.IndicatorStatus.ATTENTION)
        self._menu_item.show()
        self._menu_item.set_label("Notification: " + notif.message)

    def remove_notification(self):
        """Resets widget status to normal."""
        self._indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

if __name__ == "__main__":
    pass