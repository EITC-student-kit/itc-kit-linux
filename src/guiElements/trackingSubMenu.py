__author__ = 'Kristo Koert'
from gtk import MenuItem, ImageMenuItem, Menu
import appindicator


class TrackingSubMenu(Menu):
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

        self.sub_menu_items = [ImageMenuItem(pro_icon),
                               ImageMenuItem(neu_icon),
                               ImageMenuItem(cou_icon),
                               MenuItem("Stop"),
                               MenuItem("Reset"),
                               MenuItem("Undo")]

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