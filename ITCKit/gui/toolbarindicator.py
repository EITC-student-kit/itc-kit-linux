__author__ = "Kristo Koert"
#Dependency: gir1.2-appindicator3

from threading import ThreadError

from gi.repository import Gtk, Gdk, GLib

try:
    from gi.repository import AppIndicator3 as AppIndicator
except ImportError:
    from gi.repository import AppIndicator

from ITCKit.core.notificationHandler import NotificationHandler
from ITCKit.core.timemanager import Stopper
from ITCKit.gui.maingui import open_main_window

Gdk.threads_init()


class ToolbarIndicator():
    """Linux Gtk toolbar application indicator with a main menu containing three elements and a sub-menu attached to the
    first element of the main menu containing another 6 elements.
    """

    _tracked_time = ''

    def __init__(self):
        import os
        icon_path = os.path.dirname(os.path.abspath(__file__)) + "/icon/Icon4.png"
        self.indc = AppIndicator.Indicator.new("app-doc-menu", icon_path,
                                               AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.indc.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indc.set_attention_icon("indicator-messages-new")

        self.main_menu = MainMenu(self)
        self.sub_menu = TrackingSubMenu(self)

        self.main_menu.tracking_widget.set_submenu(TrackingSubMenu)
        self.indc.set_menu(self.main_menu)

        self.set_sub_menu_state_tracking(False)

        self._stopper = None
        self._notification_handler = NotificationHandler(self.indc, self.main_menu.notification_widget)
        self._notification_handler.start()
        GLib.timeout_add(10, self.handler_timeout)

    def handler_timeout(self):
        self.indc.set_label(self._tracked_time, '')
        return True

    def on_productivity_choice_clicked(self, widget):
        """Event handler for all three productivity type choices. Independent of choice sets sub-menu state to
        tracking.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.ImageMenuItem
        """
        self.set_sub_menu_state_tracking(True)
        self.start_stopper(widget.get_label())

    def on_stop_start_clicked(self, widget):
        """Event handler for pausing/continuing the timer.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        if widget.get_label() == "Stop":
            widget.set_label("Start")
        else:
            widget.set_label("Stop")
        self._stopper.toggle_active()

    def on_reset_clicked(self, widget):
        """Event handler for resetting the stopper.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        self.sub_menu.start_stop_widget.set_label("Stop")
        self.set_sub_menu_state_tracking(False)
        self._stopper.reset_tracking()
        self._stopper = None
        self._tracked_time = ''

    def on_notification_checked(self, widget):
        """Removes notification signs.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        widget.hide()
        self._notification_handler.remove_notification()

    @staticmethod
    def on_settings_clicked(widget):
        widget.hide()
        Gdk.threads_leave()
        open_main_window()
        Gdk.threads_enter()

    def start_stopper(self, activity_type):
        """Leaves the Gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            Gdk.threads_leave()
            self._stopper = Stopper(self, activity_type)
            self._stopper.toggle_active()
            self._stopper.start()
        except ThreadError:
            print("Threading problem in appIndicator.")
        finally:
            Gdk.threads_enter()

    def set_sub_menu_state_tracking(self, is_true=True):
        """Sets the sub-menu to the appropriate state dependent on whether or not activity tracking is going on
        or not.(This is expressed via the is_true variable)

        :param is_true: is an activity type being tracked
        :type is_true: bool
        """
        #ToDo Account for added widgets
        try:
            assert isinstance(is_true, bool)
        except AssertionError:
            print("is_true must be boolean value")
        finally:
            if is_true:
                self.sub_menu.productive_widget.hide()
                self.sub_menu.neutral_widget.hide()
                self.sub_menu.counter_productive_widget.hide()
                self.sub_menu.reset_widget.show()
                self.sub_menu.start_stop_widget.show()
            elif not is_true:
                self.sub_menu.productive_widget.show()
                self.sub_menu.neutral_widget.show()
                self.sub_menu.counter_productive_widget.show()
                self.sub_menu.reset_widget.hide()
                self.sub_menu.start_stop_widget.hide()


class MainMenu(Gtk.Menu):
    """A menu item containing three widgets."""

    def __init__(self, indicator):
        """The object is created with a reference to a AppIndicator object. It is assumed that this menu
        will be attached to that instance.

        :param indicator: an AppIndicator instance
        :type indicator: ToolbarIndicator
        """
        super(Gtk.Menu, self).__init__()

        menu_items = [Gtk.ImageMenuItem("Tracking.."),
                      Gtk.MenuItem("Settings"),
                      Gtk.ImageMenuItem("Notification!")
                      ]

        self.tracking_widget = menu_items[0]
        self.settings_widget = menu_items[1]
        self.notification_widget = menu_items[2]

        for item in menu_items:
            self.append(item)
            item.show()

        self.settings_widget.connect("activate", indicator.on_settings_clicked)
        self.notification_widget.connect("activate", indicator.on_notification_checked)
        self.notification_widget.hide()


class TrackingSubMenu(Gtk.Menu):
    """A menu item intended to be used as a sub menu."""

    def __init__(self, indicator):
        """The object is created with a reference to a AppIndicator object. It is assumed that this menu
        will be attached to a MainMenu instance in this AppIndicator.

        :param indicator: an AppIndicator instance
        :type indicator: ToolbarIndicator
        """
        super(TrackingSubMenu, self).__init__()

        #SubOptimal
        icon_indicator = AppIndicator.Indicator.new("for-retrieving-icons", "user-available",
                                                    AppIndicator.IndicatorCategory.APPLICATION_STATUS)

        pro_icon = icon_indicator.get_icon()
        icon_indicator.set_icon("user-offline")
        neu_icon = icon_indicator.get_icon()
        icon_indicator.set_icon("user-busy")
        cou_icon = icon_indicator.get_icon()

        self.sub_menu_items = [Gtk.ImageMenuItem(pro_icon).set_label("Productive"),
                               Gtk.ImageMenuItem(neu_icon).set_label("Neutral"),
                               Gtk.ImageMenuItem(cou_icon).set_label("Counter-Productive"),
                               Gtk.MenuItem("Stop"),
                               Gtk.MenuItem("Reset"),
                               Gtk.MenuItem("Undo")]

        self.productive_widget = self.sub_menu_items[0]
        self.neutral_widget = self.sub_menu_items[1]
        self.counter_productive_widget = self.sub_menu_items[2]
        self.start_stop_widget = self.sub_menu_items[3]
        self.reset_widget = self.sub_menu_items[4]
        self.undo_widget = self.sub_menu_items[5]

        self.productive_widget.set_always_show_image(True)
        self.neutral_widget.set_always_show_image(True)
        self.counter_productive_widget.set_always_show_image(True)

        for item in self.sub_menu_items:
            self.append(item)

        self.productive_widget.connect("activate", indicator.on_productivity_choice_clicked)
        self.neutral_widget.connect("activate", indicator.on_productivity_choice_clicked)
        self.counter_productive_widget.connect("activate", indicator.on_productivity_choice_clicked)
        self.start_stop_widget.connect("activate", indicator.on_stop_start_clicked)
        self.reset_widget.connect("activate", indicator.on_reset_clicked)


def activate_toolbar():
    gui = ToolbarIndicator()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()