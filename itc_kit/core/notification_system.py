__author__ = 'Kristo Koert'

from threading import Thread
from time import sleep
from gi.repository import AppIndicator3 as AppIndicator
from itc_kit.db import dbc


class NotificationHandler(Thread):
    """
    Handles checking if there are any notifications in the database that are due and raises an alarm if they are.
    """

    _notifications = []
    _notification_to_raise = []

    def __init__(self, indicator, main_menu):
        """
        Sets an Indicator object to be used as the place where a notification is raised, if needed. More info on the
        notification will be displayed on the supplied menu_item.

        :param indicator: channel for raising the notification
        :type indicator: ToolbarIndicator
        :param main_menu: Place to display more notification information
        :type main_menu: MainMenu
        """
        super(NotificationHandler, self).__init__()
        self._indicator_reference = indicator
        self._main_menu_reference = main_menu

    def run(self):
        """
        When thread is started, an endless loop ensues. Constantly checking if any notifications should be raised.
        The notifications are constantly reread into the list to assure up do date information.
        """
        while True:
            if self._main_menu_reference.notification_message == "Checked" and self._indicator_reference.notification_raised:
                self.remove_notification()
            self._notifications = dbc.get_all_notifications()
            [self._notification_to_raise.append(new_notif) for new_notif in self._get_due_notifications()]
            self._attempt_to_raise_latest_notification()
            sleep(5)

    def _get_due_notifications(self):
        """
        Return notifications that need to be raised and are not already in _notifications_to_raise.
        :rtype list
        """
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
        """
        Raises notification in Indicator and displays message in the menu item.

        param: notif: A notification
        type: notif: Notification
        """
        self._indicator_reference.notification_raised = True
        self._main_menu_reference.notification_display_widget.show()
        if notif.get_database_row()[0] == "EMail":
            self._indicator_reference.set_notification_icon("email")
            self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            self._main_menu_reference.notification_message = "EMail from: " + notif.get_database_row()[2]
        elif notif.get_database_row()[0] == "Reminder":
            self._indicator_reference.set_notification_icon("Reminder")
            self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ATTENTION)
            self._main_menu_reference.notification_message = "Reminder: " + notif.get_database_row()[2]
        else:
            raise RuntimeError("Unable to raise notification.")

    def remove_notification(self):
        """
        Hide widget and reset indicator status.
        """
        db = dbc.connect_to_db()
        db.execute("DELETE from Notification where type = ? and time = ? and message = ?",
                   self._notification_to_raise[0].get_database_row())
        db.commit()
        self._indicator_reference.indc.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self._indicator_reference.notification_raised = False
        del self._notification_to_raise[0]
        self._main_menu_reference.notification_display_widget.hide()