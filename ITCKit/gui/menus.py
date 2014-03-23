__author__ = 'kristo'

import threading
from gi.repository import Gtk, Gdk, GLib
from ITCKit.core.notificationHandler import NotificationHandler
from ITCKit.core.timemanager import Stopper
from ITCKit.settings import settings
from ITCKit.db import dbc
from ITCKit.gui import windows


class MainMenu(Gtk.Menu):

    def __init__(self, indicator):
        super(Gtk.Menu, self).__init__()

        self._indicator_reference = indicator

        menu_items = [Gtk.MenuItem("Time Manager"),
                      Gtk.MenuItem("Timetable"),
                      Gtk.MenuItem("Notifications"),
                      Gtk.MenuItem("Mail"),
                      Gtk.MenuItem("Conky"),
                      Gtk.ImageMenuItem("Display"),
                      Gtk.MenuItem("Exit")
                      ]

        self.tracking_widget = menu_items[0]
        self.tracking_widget.set_submenu(TimeManagerSubMenu())
        self.timetable_widget = menu_items[1]
        self.timetable_widget.set_submenu(TimetableSubMenu())
        self.notification_widget = menu_items[2]
        self.notification_widget.set_submenu(NotificationSubMenu())
        self.mail_widget = menu_items[3]
        self.mail_widget.set_submenu(MailSubMenu())
        self.conky_widget = menu_items[4]
        self.conky_widget.set_submenu(ConkySubMenu())
        self.notification_display_widget = menu_items[5]
        self.exit_widget = menu_items[6]

        [(self.append(item), item.show()) for item in menu_items]

        self.notification_display_widget.connect("activate", self.on_notification_checked)
        self.exit_widget.connect("activate", self.on_exit)
        self.notification_display_widget.hide()
        self.notification_handler = NotificationHandler(self, self.notification_display_widget)

    def on_notification_checked(self, widget):
        self._indicator_reference._notification_handler.remove_notification()

    def on_exit(self, widget):
        #ToDo Implement on_exit()
        raise NotImplementedError


class BaseSubMenu(Gtk.Menu):

    _state = "Not activated"

    def __init__(self):
        super(BaseSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("On/Off")]

        self.on_off_widget = menu_item[0]

        [(self.append(item), item.show()) for item in menu_item]

        self.on_off_widget.connect("activate", self.on_off_clicked)

    def on_off_clicked(self, on_off_widget):
        if self._state == "Not activated":
            self.set_menu_state("Activated")
        else:
            self.set_menu_state("Not activated")

    def set_menu_state(self, state):
        raise NotImplementedError


class TimeManagerSubMenu(BaseSubMenu):

    _stopper = None
    _display_label = ''

    def __init__(self):
        super(TimeManagerSubMenu, self).__init__()

        from ITCKit.gui.icon.build_in_icons import get_productivity_icons
        pro_icon, neu_icon, cou_icon = get_productivity_icons()

        menu_items = [Gtk.ImageMenuItem(pro_icon),
                      Gtk.ImageMenuItem(neu_icon),
                      Gtk.ImageMenuItem(cou_icon),
                      Gtk.MenuItem("Display"),
                      Gtk.MenuItem("Stop"),
                      Gtk.MenuItem("Undo")]

        self.productive_widget = menu_items[0]
        self.productive_widget.set_label("Productive")

        self.neutral_widget = menu_items[1]
        self.neutral_widget.set_label("Neutral")

        self.counter_productive_widget = menu_items[2]
        self.counter_productive_widget.set_label("Counter-Productive")

        self.display_widget = menu_items[3]
        self.stop_widget = menu_items[4]
        self.undo_widget = menu_items[5]

        self.productive_widget.set_always_show_image(True)
        self.neutral_widget.set_always_show_image(True)
        self.counter_productive_widget.set_always_show_image(True)

        if settings.get_time_manager_settings()["activated"]:
            self.set_menu_state("Activated")
        else:
            self.set_menu_state("Not activated")

        [(self.append(item)) for item in menu_items]

        self.productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.neutral_widget.connect("activate", self.on_productivity_choice_clicked)
        self.counter_productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.stop_widget.connect("activate", self.on_stop_clicked)
        self.undo_widget.connect("activate", self.on_undo_clicked)

        GLib.timeout_add(10, self.handler_timeout)

    def handler_timeout(self):
        self.display_widget.set_label(self._display_label)
        return True

    def on_productivity_choice_clicked(self, widget):
        """Event handler for all three productivity type choices. Independent of choice sets sub-menu state to
        tracking.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.ImageMenuItem
        """
        self.set_menu_state("Tracking")
        self._start_stopper(widget.get_label())

    def on_undo_clicked(self):
        #ToDo Implement tracking undo.
        pass

    def on_stop_clicked(self, widget):
        """Event handler for stopping the stopper.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        self._stopper.stop_tracking()
        self._stopper = None
        self.set_menu_state("Activated")
        #ToDo remove after testing
        print(dbc.get_all_activities())

    def _start_stopper(self, activity_type):
        """Leaves the Gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            self._stopper = Stopper(self, activity_type)
            self._stopper.start()
        except threading.ThreadError:
            print("Threading problem in Tracking sub-menu.")

    def set_menu_state(self, state):
        """Sets the sub-menu to the appropriate state.

        :param state: The current state
        :type state: str
        """
        #ToDo set on_off_widget to the bottom of menu
        if state == "Tracking":
            self.on_off_widget.hide()
            self.productive_widget.hide()
            self.neutral_widget.hide()
            self.counter_productive_widget.hide()
            self.stop_widget.show()
            self.display_widget.show()
        elif state == "Activated":
            settings.update_settings("TimeManager", "activated", True)
            self.on_off_widget.show()
            self.productive_widget.show()
            self.neutral_widget.show()
            self.counter_productive_widget.show()
            self.stop_widget.hide()
            self.display_widget.hide()
        elif state == "Not activated":
            settings.update_settings("TimeManager", "activated", False)
            self.on_off_widget.show()
            self.productive_widget.hide()
            self.neutral_widget.hide()
            self.counter_productive_widget.hide()
            self.stop_widget.hide()
            self.display_widget.hide()
        else:
            print("state parameter need to be either Tracking, Activated or Not activated")
            raise RuntimeError
        self._state = state


class TimetableSubMenu(BaseSubMenu):

    def __init__(self):
        super(TimetableSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("Manual Update"),
                     Gtk.MenuItem("Set ical URL"),
                     Gtk.MenuItem("Customize Timetable")]

        self.update_widget = menu_item[0]
        self.set_ical_url_widget = menu_item[1]
        self.customize_timetable_widget = menu_item[2]

        if settings.get_timetable_settings()["activated"]:
            self.set_menu_state("Activated")
        else:
            self.set_menu_state("Not activated")

        [(self.append(item)) for item in menu_item]

        self.update_widget.connect("activate", self.on_update_clicked)
        self.set_ical_url_widget.connect("activate", self.on_set_ical_url)

    @staticmethod
    def on_set_ical_url(widget):
        windows.open_set_ical_url()

    @staticmethod
    def on_update_clicked(widget):
        windows.open_update_timetable()

    def set_menu_state(self, state):
        if state == "Not activated":
            settings.update_settings("Timetable", "activated", False)
            self._state = "Not activated"
            self.on_off_widget.show()
            self.customize_timetable_widget.hide()
            self.set_ical_url_widget.hide()
            self.update_widget.hide()
        elif state == "Activated":
            settings.update_settings("Timetable", "activated", True)
            self._state = "Activated"
            self.on_off_widget.show()
            self.customize_timetable_widget.show()
            self.set_ical_url_widget.show()
            self.update_widget.show()


class NotificationSubMenu(BaseSubMenu):

    def __init__(self):
        super(NotificationSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("Add reminder"),
                     Gtk.MenuItem("Clear All")]

        self.add_reminder_widget = menu_item[0]
        self.clear_all_widget = menu_item[1]

        if settings.get_notification_settings()["activated"]:
            self.set_menu_state("Activated")
        else:
            self.set_menu_state("Not activated")

        [(self.append(item)) for item in menu_item]

        self.clear_all_widget.connect("activate", self.on_clear_all_clicked)
        self.add_reminder_widget.connect("activate", self.on_add_reminder_clicked)

    @staticmethod
    def on_add_reminder_clicked(widget):
        windows.open_add_reminder()

    @staticmethod
    def on_clear_all_clicked():
        dbc.remove_all_notifications()

    def set_menu_state(self, state):
        if state == "Activated":
            settings.update_settings("Notification", "activated", True)
            self._state = "Activated"
            self.add_reminder_widget.show()
            self.clear_all_widget.show()
        elif state == "Not activated":
            settings.update_settings("Notification", "activated", False)
            self._state = "Not activated"
            self.add_reminder_widget.hide()
            self.clear_all_widget.hide()


class MailSubMenu(BaseSubMenu):

    def __init__(self):
        super(MailSubMenu, self).__init__()
        menu_item = [Gtk.MenuItem("Username/Password"),
                     Gtk.MenuItem("Clear All")]

        self.set_credentials_widget = menu_item[0]
        self.clear_all_widget = menu_item[1]

        if settings.get_mail_settings()["activated"]:
            self.set_menu_state("Activated")
        else:
            self.set_menu_state("Not activated")

        [(self.append(item)) for item in menu_item]

        self.clear_all_widget.connect("activate", self.on_clear_all_clicked)
        self.set_credentials_widget.connect("activate", self.on_set_credentials_clicked)

    def on_set_credentials_clicked(self):
        #ToDo Implement on_set_credentials_clicked
        pass

    def on_clear_all_clicked(self):
        #ToDo Implement on_clear_all_clicked
        pass

    def set_menu_state(self, state):
        if state == "Not activated":
            settings.update_settings("Mail", "activated", False)
            self._state = "Not activated"
            self.clear_all_widget.hide()
            self.set_credentials_widget.hide()
        else:
            settings.update_settings("Mail", "activated", True)
            self._state = "Activated"
            self.clear_all_widget.show()
            self.set_credentials_widget.show()


class ConkySubMenu(BaseSubMenu):

    def __init__(self):
        super(ConkySubMenu, self).__init__()
        menu_item = [Gtk.MenuItem("Set Color"),
                     Gtk.MenuItem("Display Settings")]

        self.set_color_widget = menu_item[0]
        self.display_settings_widget = menu_item[1]

        if settings.get_conky_settings()["activated"]:
            [item.show() for item in menu_item]

        [(self.append(item)) for item in menu_item]

        self.set_color_widget.connect("activate", self.on_set_color_clicked)
        self.display_settings_widget.connect("activate", self.on_display_settings_clicked)

    def on_set_color_clicked(self):
        #ToDo implement on_set_color_clicked
        pass

    def on_display_settings_clicked(self):
        #ToDo implement on_set_color_clicked
        pass

    def set_menu_state(self, state):
        if state == "Not activated":
            settings.update_settings("Conky", "activated", False)
            self._state = "Not activated"
            self.display_settings_widget.hide()
            self.set_color_widget.hide()
        else:
            settings.update_settings("Conky", "activated", True)
            self._state = "Activated"
            self.display_settings_widget.show()
            self.set_color_widget.show()