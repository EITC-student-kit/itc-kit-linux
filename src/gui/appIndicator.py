__author__ = "Kristo Koert"

import gtk
import appindicator
from threading import ThreadError

from src.notificationtracking import NotificationHandler
from src.timemanager import Stopper
from mainMenu import MainMenu
from trackingSubMenu import TrackingSubMenu


gtk.gdk.threads_init()


class AppIndicator(appindicator.Indicator):
    """Linux gtk toolbar application indicator with a main menu containing three elements and a sub-menu attached to the
    first element of the main menu containing another 6 elements.
    """

    def __init__(self):
        from src.utilityFunctions import UtilityFunctions
        icon_path = UtilityFunctions.own_path() + "/icon/Ico4.png"
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