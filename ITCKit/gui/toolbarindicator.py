__author__ = "Kristo Koert"
#Dependency: gir1.2-appindicator3

from gi.repository import Gtk, Gdk
from ITCKit.settings import settings
try:
    from gi.repository import AppIndicator3 as AppIndicator
except ImportError:
    from gi.repository import AppIndicator

from ITCKit.gui.menus import MainMenu


class ToolbarIndicator():

    _tracked_time = ''
    notification_raised = False

    def __init__(self):
        icon_path = settings.get_other_settings()["icon_path"]
        self.indc = AppIndicator.Indicator.new("app-doc-menu", icon_path,
                                               AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.indc.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indc.set_attention_icon("ubuntuone-client-offline")

        self.main_menu = MainMenu(self)
        self.indc.set_menu(self.main_menu)

    def set_notification_icon(self, typ):
        if typ == "email":
            self.indc.set_attention_icon("indicator-messages-new")
        else:
            self.indc.set_attention_icon("ubuntuone-client-offline")


def activate_toolbar():
    gui = ToolbarIndicator()
    return gui

if __name__ == "__main__":
    activate_toolbar()