__author__ = 'kristo'

from threading import ThreadError

from gi.repository import Gtk, Gdk, GLib

from ITCKit.core.notificationHandler import NotificationHandler
from ITCKit.core.timemanager import Stopper
from ITCKit.settings.settings import *


class MainMenu(Gtk.Menu):

    def __init__(self):
        super(Gtk.Menu, self).__init__()

        menu_items = [Gtk.MenuItem("Time Manager"),
                      Gtk.MenuItem("Timetable"),
                      Gtk.MenuItem("Notifications"),
                      Gtk.MenuItem("Mail"),
                      Gtk.MenuItem("Conky"),
                      Gtk.ImageMenuItem("Display"),
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

        [(self.append(item), item.show()) for item in menu_items]

        self.notification_display_widget.connect("activate", self.on_notification_checked)
        self.notification_display_widget.hide()
        self.notification_handler = NotificationHandler(self, self.notification_display_widget)

    def on_notification_checked(self, widget):
        self._notification_handler.remove_notification()


class BaseSubMenu(Gtk.Menu):

    def __init__(self):
        super(BaseSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("On/Off")]

        self.on_off_widget = menu_item[0]

        [(self.append(item), item.show()) for item in menu_item]

        self.on_off_widget.connect("activate", self.on_off_clicked)

    def on_off_clicked(self):
        #ToDo Implement on_off for all menus
        pass


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

        #ToDo Account for On/Off widget

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

        if get_time_manager_settings()["Activated"]:
            [item.show() for item in menu_items]

        [(self.append(item)) for item in menu_items]

        self.productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.neutral_widget.connect("activate", self.on_productivity_choice_clicked)
        self.counter_productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.stop_widget.connect("activate", self.on_stop_clicked)
        self.undo_widget.connect("activate", self.on_undo_clicked)

        self.display_widget.hide()
        self.stop_widget.hide()
        self.undo_widget.hide()

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
        self._set_sub_menu_state_tracking(True)
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
        self._set_sub_menu_state_tracking(False)
        #ToDo remove after testing
        from ITCKit.db import dbc
        print(dbc.get_all_activities())

    def _start_stopper(self, activity_type):
        """Leaves the Gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            Gdk.threads_leave()
            self._stopper = Stopper(self, activity_type)
            self._stopper.start()
        except ThreadError:
            print("Threading problem in Tracking sub-menu.")
        finally:
            Gdk.threads_enter()

    def _set_sub_menu_state_tracking(self, is_tracking=True):
        """Sets the sub-menu to the appropriate state dependent on whether or not activity tracking is going on
        or not.(This is expressed via the is_true variable)

        :param is_tracking: is an activity type being tracked
        :type is_tracking: bool
        """
        #ToDo Account for any added widgets
        try:
            assert isinstance(is_tracking, bool)
        except AssertionError:
            print("is_true must be boolean value")
        finally:
            if is_tracking:
                self.productive_widget.hide()
                self.neutral_widget.hide()
                self.counter_productive_widget.hide()
                self.stop_widget.show()
                self.display_widget.show()
            elif not is_tracking:
                self.productive_widget.show()
                self.neutral_widget.show()
                self.counter_productive_widget.show()
                self.stop_widget.hide()
                self.display_widget.hide()


class TimetableSubMenu(BaseSubMenu):

    def __init__(self):
        super(TimetableSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("Manual Update"),
                     Gtk.MenuItem("Set ical URL"),
                     Gtk.MenuItem("Customize Timetable")]

        self.update_widget = menu_item[0]
        self.set_ical_url_widget = menu_item[1]
        self.customize_timetable_widget = menu_item[2]

        if get_timetable_settings()["Activated"]:
            [item.show() for item in menu_item]

        [(self.append(item)) for item in menu_item]

        self.update_widget.connect("activate", self.on_update_clicked)
        self.set_ical_url_widget.connect("activate", self.on_set_ical_url)

    def on_set_ical_url(self):
        #ToDo implement on_set_ical_url
        pass

    def on_update_clicked(self):
        #ToDo implement on_update_clicked
        pass


class NotificationSubMenu(BaseSubMenu):

    def __init__(self):
        super(NotificationSubMenu, self).__init__()

        menu_item = [Gtk.MenuItem("Add reminder"),
                     Gtk.MenuItem("Clear All")]

        self.add_reminder_widget = menu_item[0]
        self.clear_all_widget = menu_item[1]

        if get_notification_settings()["Activated"]:
            [item.show() for item in menu_item]

        [(self.append(item)) for item in menu_item]

        self.clear_all_widget.connect("activate", self.on_clear_all_clicked)
        self.add_reminder_widget.connect("activate", self.on_add_reminder_clicked)

    def on_add_reminder_clicked(self):
        #ToDo implement on_add_reminder_clicked
        pass

    def on_clear_all_clicked(self):
        #ToDo implement on_clear_all_clicked
        pass


class MailSubMenu(BaseSubMenu):

    def __init__(self):
        super(MailSubMenu, self).__init__()
        menu_item = [Gtk.MenuItem("Username/Password"),
                     Gtk.MenuItem("Clear All")]

        self.set_credentials = menu_item[0]
        self.clear_all_widget = menu_item[1]

        if get_mail_settings()["Activated"]:
            [item.show() for item in menu_item]

        [(self.append(item)) for item in menu_item]

        self.clear_all_widget.connect("activate", self.on_clear_all_clicked)
        self.set_credentials.connect("activate", self.on_set_credentials_clicked)

    def on_set_credentials_clicked(self):
        #ToDo Implement on_set_credentials_clicked
        pass


class ConkySubMenu(BaseSubMenu):
    def __init__(self):
        super(ConkySubMenu, self).__init__()
        menu_item = [Gtk.MenuItem("Set Color"),
                     Gtk.MenuItem("Display Settings")]

        self.set_color_widget = menu_item[0]
        self.display_settings_widget = menu_item[1]

        if get_conky_settings()["Activated"]:
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