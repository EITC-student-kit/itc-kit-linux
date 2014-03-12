__author__ = "Kristo Koert"

import gtk
import appindicator
from threading import ThreadError
from ITCKit.core.notificationHandler import NotificationHandler
from ITCKit.core.timemanager import Stopper

gtk.gdk.threads_init()


class AppIndicator(appindicator.Indicator):
    """Linux gtk toolbar application indicator with a main menu containing three elements and a sub-menu attached to the
    first element of the main menu containing another 6 elements.
    """

    def __init__(self):
        import os
        icon_path = os.path.dirname(os.path.abspath(__file__)) + "/ico4.png"
        super(AppIndicator, self).__init__("app-doc-menu", icon_path,
                                           appindicator.CATEGORY_APPLICATION_STATUS)

        self.set_status(appindicator.STATUS_ACTIVE)
        self.set_attention_icon("indicator-messages-new")

        self.main_menu = MainMenu(self)
        self.sub_menu = TrackingSubMenu(self)

        self.main_menu.tracking_widget.set_submenu(self.sub_menu)

        self.set_sub_menu_state_tracking(False)

        self.set_menu(self.main_menu)

        self._stopper = None
        self._notification_handler = NotificationHandler(self, self.main_menu.notification_widget)
        self._notification_handler.start()

    def on_productivity_choice_clicked(self, widget):
        """Event handler for all three productivity type choices. Independent of choice sets sub-menu state to
        tracking.

        :param widget: the widget that triggered this event handler
        :type widget: gtk.ImageMenuItem
        """
        self.set_sub_menu_state_tracking(True)
        self.start_stopper()

    def on_stop_clicked(self, widget):
        """Event handler for stopping the timer.

        :param widget: the widget that triggered this event handler
        :type widget: gtk.MenuItem
        """
        if widget.get_label() == "Stop":
            widget.set_label("Start")
        else:
            widget.set_label("Stop")
        self._stopper.toggle_active()

    def on_reset_clicked(self, widget):
        """Event handler for resetting the stopper.

        :param widget: the widget that triggered this event handler
        :type widget: gtk.MenuItem
        """
        self.sub_menu.stop_widget.set_label("Stop")
        self.set_sub_menu_state_tracking(False)
        widget.hide()
        self.reset_stopper()

    def start_stopper(self):
        """Leaves the gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            gtk.threads_leave()
            self._stopper = Stopper(self)
            self._stopper.toggle_active()
            self._stopper.start()
        except ThreadError:
            print("Threading problem in appIndicator.")
        finally:
            gtk.threads_enter()

    def reset_stopper(self):
        """Deals with resetting the Stopper object via stopping it and removing the reference to it. The indicators
        label is also reset to empty.
        """
        self._stopper.stop_tracking()
        self._stopper = None
        self.set_label("")

    def on_more_clicked(self, widget):
        raise NotImplementedError

    def notification_checked(self, widget):
        """Removes notification signs.

        :param widget: the widget that triggered this event handler
        :type widget: gtk.MenuItem
        """
        widget.hide()
        self._notification_handler.remove_notification()

    def set_sub_menu_state_tracking(self, is_true=True):
        """Sets the sub-menu to the appropriate state dependent on whether or not activity tracking is going on
        or not.(This is expressed via the is_true variable)

        :param is_true: is an activity type being tracked
        :type is_true: bool
        """
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
                self.sub_menu.stop_widget.show()
            elif not is_true:
                self.sub_menu.productive_widget.show()
                self.sub_menu.neutral_widget.show()
                self.sub_menu.counter_productive_widget.show()
                self.sub_menu.reset_widget.hide()
                self.sub_menu.stop_widget.hide()

if __name__ == "__main__":
    gui = AppIndicator()
    gtk.threads_enter()
    gtk.main()
    gtk.threads_leave()


class MainMenu(gtk.Menu):
    """A menu item containing three widgets."""

    def __init__(self, indicator):
        """The object is created with a reference to a AppIndicator object. It is assumed that this menu
        will be attached to that instance.

        :param indicator: an AppIndicator instance
        :type indicator: AppIndicator
        """
        super(gtk.Menu, self).__init__()

        menu_items = [gtk.ImageMenuItem("Tracking.."),
                      gtk.MenuItem("More"),
                      gtk.ImageMenuItem("Notification!")
                      ]

        self.tracking_widget = menu_items[0]
        self.more_widget = menu_items[1]
        self.notification_widget = menu_items[2]

        for item in menu_items:
            self.append(item)
            item.show()

        self.more_widget.connect("activate", indicator.on_more_clicked)
        self.notification_widget.connect("activate", indicator.notification_checked)
        self.notification_widget.hide()


class TrackingSubMenu(gtk.Menu):
    """A menu item intended to be used as a sub menu."""

    def __init__(self, indicator):
        """The object is created with a reference to a AppIndicator object. It is assumed that this menu
        will be attached to a MainMenu instance in this AppIndicator.

        :param indicator: an AppIndicator instance
        :type indicator: AppIndicator
        """
        super(TrackingSubMenu, self).__init__()

        #Only used to retrieve icons, probably a better way to do this.
        icon_indicator = appindicator.Indicator("for-retrieving-icons", "user-available",
                                                appindicator.CATEGORY_APPLICATION_STATUS)

        pro_icon = icon_indicator.get_icon()
        icon_indicator.set_icon("user-offline")
        neu_icon = icon_indicator.get_icon()
        icon_indicator.set_icon("user-busy")
        cou_icon = icon_indicator.get_icon()

        self.sub_menu_items = [gtk.ImageMenuItem(pro_icon),
                               gtk.ImageMenuItem(neu_icon),
                               gtk.ImageMenuItem(cou_icon),
                               gtk.MenuItem("Stop"),
                               gtk.MenuItem("Reset"),
                               gtk.MenuItem("Undo")]

        #Probably a better way to set the labels on instance creation.
        self.sub_menu_items[0].set_label("Productive")
        self.sub_menu_items[1].set_label("Neutral")
        self.sub_menu_items[2].set_label("Counter-Productive")

        self.productive_widget = self.sub_menu_items[0]
        self.neutral_widget = self.sub_menu_items[1]
        self.counter_productive_widget = self.sub_menu_items[2]
        self.stop_widget = self.sub_menu_items[3]
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
        self.stop_widget.connect("activate", indicator.on_stop_clicked)
        self.reset_widget.connect("activate", indicator.on_reset_clicked)


