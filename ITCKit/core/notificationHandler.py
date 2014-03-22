__author__ = 'Kristo Koert'

#ToDo re-implement to work with new build

from threading import Thread
from time import sleep

from gi.repository import AppIndicator3 as AppIndicator

from ITCKit.db import dbc


class NotificationHandler(Thread):
    """Handles checking if there are any notifications in a database that are due and raises an alarm if they are."""

    _notifications = []

    def __init__(self, indicator, menu_item):
        """Sets an Indicator object to be used as the place where a notification is raised, if needed. More info on the
        notification will be displayed on the menu_item.

        :param indicator: channel for raising the notification
        :type indicator: ToolbarIndicator
        :param menu_item: Place to display more notification information
        :type menu_item: gtk.ImageMenuItem
        """
        super(NotificationHandler, self).__init__()
        self._indicator = indicator
        self._menu_item = menu_item

    def run(self):
        """When thread is started, an endless loop ensues. Constantly checking if any notifications should be raised.
        The notifications are constantly reread into the list to assure up do date information."""
        #ToDo Performance Hit for constant rereading?
        while True:
            self._notifications = self._get_notifications()
            self._check_notifications()
            sleep(10)

    def _check_notifications(self):
        """Checks if any notifications should be triggered."""
        if self._notifications[0] is not None:
            for notif in self._notifications:
                if notif.is_due():
                    self._raise_notification(notif)
                    self._notifications.remove(notif)

    @staticmethod
    def _get_notifications():
        """Gets notifications from database"""
        return dbc.get_all_notifications()

    def _raise_notification(self, notif):
        """Raises notification in Indicator passed as __init__ parameter and displays message in the widget.

        param: notif: A notification
        type: notif: Notification
        """
        self._menu_item.show()
        if notif.get_database_row()[0] == "Mail":
            #ToDo switch ATTENTION icons to mail
            self._indicator.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            self._menu_item.set_label("Mail from: " + notif.message)
        if notif.get_database_row()[0] == "Reminder":
            #ToDo switch ATTENTION icons to reminder
            self._indicator.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            self._menu_item.set_label("Reminder: " + notif.message)

    def remove_notification(self):
        """Hide widget and reset indicator status."""
        self._indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self._menu_item.hide()


if __name__ == "__main__":
    pass