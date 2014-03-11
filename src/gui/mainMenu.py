__author__ = 'Kristo Koert'
from gtk import MenuItem, ImageMenuItem, Menu


class MainMenu(Menu):
    """A menu item containing three widgets."""

    def __init__(self, indicator):
        """The object is created with a reference to a AppIndicator object. It is assumed that this menu
        will be attached to that instance.

        :param indicator: an AppIndicator instance
        :type indicator: AppIndicator
        """
        super(Menu, self).__init__()

        menu_items = [ImageMenuItem("Tracking.."),
                      MenuItem("More"),
                      ImageMenuItem("Notification!")
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