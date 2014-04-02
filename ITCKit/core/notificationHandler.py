__author__ = 'Kristo Koert'

from threading import Thread
from time import sleep
from gi.repository import AppIndicator3 as AppIndicator
from ITCKit.db import dbc


class NotificationHandler(Thread):
    """Handles checking if there are any notifications in a database that are due and raises an alarm if they are."""

    _notifications = []
    _notification_to_raise = []

    def __init__(self, indicator, menu_item):
        """Sets an Indicator object to be used as the place where a notification is raised, if needed. More info on the
        notification will be displayed on the menu_item.

        :param indicator: channel for raising the notification
        :type indicator: ToolbarIndicator
        :param menu_item: Place to display more notification information
        :type menu_item: ImageMenuItem
        """
        super(NotificationHandler, self).__init__()
        self._indicator_reference = indicator
        self._menu_item_reference = menu_item

    def run(self):
        """When thread is started, an endless loop ensues. Constantly checking if any notifications should be raised.
        The notifications are constantly reread into the list to assure up do date information."""
        while True:
            self._notifications = dbc.get_all_notifications()
            [self._notification_to_raise.append(new_notif) for new_notif in self._get_due_notifications()]
            self._attempt_to_raise_latest_notification()
            sleep(1)

    def _get_due_notifications(self):
        """Return notifications that need to be raised and are not already in _notifications_to_raise.
        :rtype Notification"""
        new_notifs_to_raise = []
        if len(self._notifications) != 0:
            for notif in self._notifications:
                if notif.is_due() and (notif not in self._notification_to_raise):
                        new_notifs_to_raise.append(notif)
        return new_notifs_to_raise

    def _attempt_to_raise_latest_notification(self):
        if len(self._notification_to_raise) != 0 and not self._indicator_reference.notification_raised:
            self._raise_notification(self._notification_to_raise[0])

    def _raise_notification(self, notif):
        """Raises notification in Indicator and displays message in the menu item.

        param: notif: A notification
        type: notif: Notification
        """
        self._indicator_reference.notification_raised = True
        self._menu_item_reference.show()
        if notif.get_database_row()[0] == "Mail":
            #ToDo switch ATTENTION icons to mail
            self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            self._menu_item_reference.set_label("Mail from: " + notif.message)
        if notif.get_database_row()[0] == "Reminder":
            #ToDo switch ATTENTION icons to reminder
            self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            #DebuggingAid
            print("Reminder object -> ", notif)
            print("Get Reminder Name -> ", notif.get_database_row()[2])
            self._menu_item_reference.set_label("Reminder: " + notif.get_database_row()[2])
        else:
            print("Unable to raise notification.")
            raise RuntimeError

    def remove_notification(self):
        """Hide widget and reset indicator status."""
        db = dbc.connect_to_db()
        #DebuggingAid
        print("-------------------------------------------------------------------------")
        print("db before: ")
        [print(n) for n in dbc.get_all_notifications()]
        print("to_raise before: ")
        [print(n) for n in self._notification_to_raise]
        db.execute("DELETE from Notification where type = ? and time = ? and message = ?",
                   self._notification_to_raise[0].get_database_row())
        db.commit()
        self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self._indicator_reference.notification_raised = False
        del self._notification_to_raise[0]
        self._menu_item_reference.hide()
        #DebuggingAid
        print("db after: ")
        [print(n) for n in dbc.get_all_notifications()]
        print("to_raise after: ")
        [print(n) for n in self._notification_to_raise]


if __name__ == "__main__":
    pass