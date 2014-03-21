__author__ = 'kristo'

from threading import ThreadError

from gi.repository import Gtk, Gdk, GLib

from ITCKit.gui.built_in_icons import pro_icon, neu_icon, cou_icon
from ITCKit.core.timemanager import Stopper


class MainMenu(Gtk.Menu):

    def __init__(self):
        super(Gtk.Menu, self).__init__()

        menu_items = [Gtk.MenuItem("Time Manager"),
                      Gtk.MenuItem("Timetable"),
                      Gtk.MenuItem("Mail"),
                      Gtk.MenuItem("Conky"),
                      Gtk.ImageMenuItem("Notifications"),
                      ]

        self.tracking_widget = menu_items[0]
        self.set_submenu(TrackingSubMenu())
        self.timetable_widget = menu_items[1]
        self.mail_widget = menu_items[2]
        self.conky_widget = menu_items[3]
        self.notification_widget = menu_items[4]

        [(self.append(item), item.show()) for item in menu_items]

        self.notification_widget.hide("activate", self.on_notification_checked)

        def on_notification_checked(self, widget):
            """Removes notification signs.

            :param widget: the widget that triggered this event handler
            :type widget: Gtk.MenuItem
            """
            widget.hide()
            self._notification_handler.remove_notification()


class TrackingSubMenu(Gtk.Menu):

    _stopper = None
    _tracked_time = ''

    def __init__(self):
        """"""
        super(TrackingSubMenu, self).__init__()

        sub_menu_items = [Gtk.ImageMenuItem(pro_icon, label="Productive"),
                          Gtk.ImageMenuItem(neu_icon, label="Neutral"),
                          Gtk.ImageMenuItem(cou_icon, label="Counter-Productive"),
                          Gtk.MenuItem("Display"),
                          Gtk.MenuItem("Stop"),
                          Gtk.MenuItem("Undo")]

        self.productive_widget = sub_menu_items[0]
        #self.productive_widget.set_label("Productive")

        self.neutral_widget = sub_menu_items[1]
        #self.neutral_widget.set_label("Neutral")

        self.counter_productive_widget = sub_menu_items[2]
        #self.counter_productive_widget.set_label("Counter-Productive")

        self.display = sub_menu_items[3]
        self.stop = sub_menu_items[4]
        self.undo_widget = sub_menu_items[5]

        self.productive_widget.set_always_show_image(True)
        self.neutral_widget.set_always_show_image(True)
        self.counter_productive_widget.set_always_show_image(True)

        [self.append(item) for item in sub_menu_items]

        self.productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.neutral_widget.connect("activate", self.on_productivity_choice_clicked)
        self.counter_productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.stop.connect("activate", self.on_stop_clicked)
        self.undo_widget.connect("activate", self.on_undo_clicked)
        GLib.timeout_add(10, self.handler_timeout)

    def handler_timeout(self):
        self.display.set_label(self._tracked_time, '')
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
        pass

    def on_stop_clicked(self, widget):
        """Event handler for pausing/continuing the timer.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        self._stopper.stop_tracking()
        self._stopper = None
        self._tracked_time = ''
        #ToDo remove after testing
        from ITCKit.db import dbc
        print(dbc.get_all_activities())

    def _start_stopper(self, activity_type):
        """Leaves the Gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            Gdk.threads_leave()
            self._stopper = Stopper(self.display, activity_type)
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
        #ToDo Account for added widgets
        try:
            assert isinstance(is_tracking, bool)
        except AssertionError:
            print("is_true must be boolean value")
        finally:
            if is_tracking:
                self.productive_widget.hide()
                self.neutral_widget.hide()
                self.counter_productive_widget.hide()
                self.stop.show()
            elif not is_tracking:
                self.productive_widget.show()
                self.neutral_widget.show()
                self.counter_productive_widget.show()
                self.stop.hide()


class ConkySubMenu(Gtk.Menu):

    def __init__(self):
        pass


class NotificationSubMenu(Gtk.Menu):

    def __init__(self):
        pass
