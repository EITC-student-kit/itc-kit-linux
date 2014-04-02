__author__ = "Kristo Koert"
#Dependency: gir1.2-appindicator3

from gi.repository import Gtk, Gdk

try:
    from gi.repository import AppIndicator3 as AppIndicator
except ImportError:
    from gi.repository import AppIndicator

from ITCKit.core.notificationHandler import NotificationHandler
from ITCKit.gui.menus import MainMenu


class ToolbarIndicator():

    _tracked_time = ''
    notification_raised = False

    def __init__(self):
        import os
        icon_path = os.path.dirname(os.path.abspath(__file__)) + "/icon/Icon4.png"
        self.indc = AppIndicator.Indicator.new("app-doc-menu", icon_path,
                                               AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.indc.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indc.set_attention_icon("indicator-messages-new")

        self.main_menu = MainMenu(self)
        self.indc.set_menu(self.main_menu)

        self.notification_handler = NotificationHandler(self, self.main_menu.notification_display_widget)
        self.notification_handler.start()

    def set_notification_icon(self):
        #ToDo implement set_notification_icon
        raise NotImplementedError


def activate_toolbar():
    Gdk.threads_init()
    gui = ToolbarIndicator()
    Gtk.main()

if __name__ == "__main__":
    activate_toolbar()