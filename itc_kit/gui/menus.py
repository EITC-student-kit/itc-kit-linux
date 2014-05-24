__author__ = 'Kristo Koert'

import threading
from gi.repository import Gtk, Gdk, GLib
from itc_kit.core.timemanager import Stopper
from itc_kit.settings import settings
from itc_kit.db import dbc
from itc_kit.gui import windows

#Used to generated menu widgets dynamically
NR_OF_PLUGINS = 0


def add_plugin():
    global NR_OF_PLUGINS
    NR_OF_PLUGINS += 1


def get_state(sub_menu):
    """
    :return The state of a plugin
    :rtype bool
    """
    key = "activated"
    states = {TimetableSubMenu.__name__: settings.get_timetable_settings()[key],
              MailSubMenu.__name__: settings.get_email_settings()[key],
              NotificationSubMenu.__name__: settings.get_notification_settings()[key],
              TimeManagerSubMenu.__name__: settings.get_time_manager_settings()[key],
              ConkySubMenu.__name__: settings.get_conky_settings()[key]}
    return states[sub_menu]


class MainMenu(Gtk.Menu):
    """
    This class creates the main menu in the application indicator

    Many of the variables that are created in this class are used in the submenus to create the proper menu setup.
    """

    #Used as a way to notify notification_system that a notification has been checked
    notification_message = "Checked"

    def __init__(self, indicator):
        super(Gtk.Menu, self).__init__()

        self._indicator_reference = indicator
        self.sub_menus = dict()

        self.menu_items = [Gtk.MenuItem("Timetable"),
                           Gtk.MenuItem("EMail"),
                           Gtk.MenuItem("Notifications"),
                           Gtk.MenuItem("Time Manager"),
                           Gtk.MenuItem("Conky"),
                           Gtk.MenuItem("Plugins"),
                           Gtk.ImageMenuItem("Notification Display"),
                           Gtk.ImageMenuItem("Exit")]

        #Creates a dictionary where the keys are the name of a class and the values are instances
        for sub_menu in BaseSubMenu.__subclasses__():
            if sub_menu.__name__ != "PluginSubMenu":
                self.sub_menus[sub_menu.__name__] = sub_menu()

        self.sub_menus["PluginSubMenu"] = PluginSubMenu(self)

        self.timetable_widget = self.menu_items[0]
        self.timetable_widget.set_submenu(self.sub_menus[TimetableSubMenu.__name__])
        self.email_widget = self.menu_items[1]
        self.email_widget.set_submenu(self.sub_menus[MailSubMenu.__name__])
        self.notification_widget = self.menu_items[2]
        self.notification_widget.set_submenu(self.sub_menus[NotificationSubMenu.__name__])
        self.tracking_widget = self.menu_items[3]
        self.tracking_widget.set_submenu(self.sub_menus[TimeManagerSubMenu.__name__])
        self.conky_widget = self.menu_items[4]
        self.conky_widget.set_submenu(self.sub_menus[ConkySubMenu.__name__])
        self.plugins_widget = self.menu_items[5]
        self.plugins_widget.set_submenu(self.sub_menus[PluginSubMenu.__name__])
        self.notification_display_widget = self.menu_items[6]
        self.exit_widget = self.menu_items[7]

        [(self.append(item), item.show()) for item in self.menu_items]

        self.notification_display_widget.connect("activate", self.on_notification_checked)
        self.exit_widget.connect("activate", self.on_exit)
        self.notification_display_widget.hide()
        GLib.timeout_add(10, self.handler_timeout)
        GLib.timeout_add(500, self.handler_timeout2)

    def handler_timeout(self):
        self.notification_display_widget.set_label(self.notification_message)
        return True

    def handler_timeout2(self):
        """
        Sets the menu state, what widgets should be shown or hidden
        """
        global NR_OF_PLUGINS
        for i in range(NR_OF_PLUGINS):
            if get_state(self.menu_items[i].get_submenu().__class__.__name__):
                self.menu_items[i].show()
            else:
                self.menu_items[i].hide()
        return True

    def on_notification_checked(self, widget):
        self.notification_message = "Checked"

    def on_exit(self, widget):
        import os
        cmd = "sh " + os.getenv("HOME") + "/.itc-kit/kill_program.sh"
        os.system(cmd)


class BaseSubMenu(Gtk.Menu):
    """
    Classes inheriting from this class are expected to be added to plugins
    """
    menu_item_lbl = None

    def __init__(self, identity, lbl):
        super(Gtk.Menu, self).__init__()
        self.identity = identity
        self.menu_item_lbl = lbl

    def set_active_in_settings(self, state):
        settings.update_settings(self.menu_item_lbl, "activated", state)


class PluginSubMenu(BaseSubMenu):
    """
    This class generates a submenu of the available plugins by using the variables created on the creation
    of the MainMenu.
    """

    def __init__(self, main_menu_ref):
        super(PluginSubMenu, self).__init__(self.__class__.__name__, "Plugins")
        self.main_menu_ref = main_menu_ref
        self.plugins = self.make_submenus_dict()
        self.menu_items, self.menu_refs = self.make_menu()

        for widget in self.menu_items:
            self.append(widget)

        self.timetable_widget = self.menu_items[0]
        self.email_widget = self.menu_items[1]
        self.notifications_widget = self.menu_items[2]
        self.timemanager_widget = self.menu_items[3]
        self.conky_widget = self.menu_items[4]

        for it in self.menu_items:
            it.show()

        for widget in self.menu_items:
            widget.connect("activate", self.click_plugin)

    def click_plugin(self, widget):
        ref_indx = self.menu_items.index(widget)
        state = get_state(self.menu_refs[ref_indx].__class__.__name__)
        if state:
            self.menu_refs[ref_indx].set_active_in_settings(False)
        elif not state:
            if isinstance(self.menu_refs[ref_indx], MailSubMenu):
                windows.open_set_credentials()
            self.menu_refs[ref_indx].set_active_in_settings(True)
        else:
            print("State:", state)
            raise RuntimeError

    def make_menu(self):
        """
        Creates a menu based on all the classes that have inherited BaseSubMenu with some
        manually inserted exceptions.

        :rtype list
        """
        menu = []
        refs = []
        for key in self.plugins:
            is_active = self.plugins[key]["active?"]
            ref = self.plugins[key]["menu_ref"]
            if is_active:
                lbl = ref.menu_item_lbl
                menu.append(Gtk.CheckMenuItem(lbl))
                refs.append(ref)
                menu[-1].set_active(True)
            else:
                lbl = ref.menu_item_lbl
                menu.append(Gtk.CheckMenuItem(lbl))
                refs.append(ref)
        return menu, refs

    def make_submenus_dict(self):
        """
        Creates a dictionary where the keys are names of the classes that have inherited BaseSubMenu (with some exceptions)
        The corresponding value is another dictonary with the keys "active?" which returns whether the menu is
        currently active and "menu_ref" which returns the refrence for the menu.

        :rtype dict
        """

        d = dict()
        for key in self.main_menu_ref.sub_menus.keys():
            d[key] = {"active?": get_state(key), "menu_ref": self.main_menu_ref.sub_menus[key]}
        return d


class TimeManagerSubMenu(BaseSubMenu):

    _stopper = None
    _display_label = ''

    def __init__(self):
        add_plugin()
        super(TimeManagerSubMenu, self).__init__(self.__class__.__name__, "Time manager")

        from itc_kit.gui.icons.build_in_icons import get_productivity_icons

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

        [(self.append(item)) for item in menu_items]

        self.productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.neutral_widget.connect("activate", self.on_productivity_choice_clicked)
        self.counter_productive_widget.connect("activate", self.on_productivity_choice_clicked)
        self.stop_widget.connect("activate", self.on_stop_clicked)
        self.undo_widget.connect("activate", self.on_undo_clicked)

        self.set_menu_state2("activated")

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
        self.set_menu_state2("tracking")
        self._start_stopper(widget.get_label())

    def on_undo_clicked(self):
        #ToDo Implement tracking undo.
        raise NotImplementedError

    def on_stop_clicked(self, widget):
        """Event handler for stopping the stopper.

        :param widget: the widget that triggered this event handler
        :type widget: Gtk.MenuItem
        """
        self._stopper.stop_tracking()
        self._stopper = None
        self.set_menu_state2("activated")

    def _start_stopper(self, activity_type):
        """Leaves the Gtk thread, creates a Stopper object there that is referenced in this object and starts it."""
        try:
            self._stopper = Stopper(self, activity_type)
            self._stopper.start()
        except threading.ThreadError:
            print("Threading problem in Tracking sub-menu.")

    def set_menu_state2(self, state):
        """Sets the sub-menu to the appropriate state.

        :param state: The current state
        :type state: str
        """
        if state == "tracking":
            self.productive_widget.hide()
            self.neutral_widget.hide()
            self.counter_productive_widget.hide()
            self.stop_widget.show()
            self.display_widget.show()
        elif state == "activated":
            self.productive_widget.show()
            self.neutral_widget.show()
            self.counter_productive_widget.show()
            self.stop_widget.hide()
            self.display_widget.hide()
            #self.undo_widget.hide()
        else:
            print("state parameter need to be either tracking or activated.")
            raise RuntimeError


class TimetableSubMenu(BaseSubMenu):

    def __init__(self):
        add_plugin()
        super(TimetableSubMenu, self).__init__(self.__class__.__name__, "Timetable")

        menu_items = [Gtk.MenuItem("Update"),
                      Gtk.MenuItem("Set ical URL"),
                      Gtk.MenuItem("Customize Timetable")]

        for it in menu_items:
            it.show()

        self.update_widget = menu_items[0]
        self.set_ical_url_widget = menu_items[1]
        self.customize_timetable_widget = menu_items[2]

        [(self.append(item)) for item in menu_items]

        self.update_widget.connect("activate", self.on_update_clicked)
        self.set_ical_url_widget.connect("activate", self.on_set_ical_url)
        self.customize_timetable_widget.connect("activate", self.on_customize_timetable_clicked)

    @staticmethod
    def on_set_ical_url(widget):
        windows.open_set_ical_url()

    @staticmethod
    def on_update_clicked(widget):
        windows.open_update_timetable()

    @staticmethod
    def on_customize_timetable_clicked(widget):
        windows.open_customize_timetable()


class NotificationSubMenu(BaseSubMenu):

    def __init__(self):
        add_plugin()
        super(NotificationSubMenu, self).__init__(self.__class__.__name__, "Notification")

        menu_items = [Gtk.MenuItem("Add reminder"),
                      Gtk.MenuItem("Clear All")]

        for it in menu_items:
            it.show()

        self.add_reminder_widget = menu_items[0]
        self.clear_all_widget = menu_items[1]

        [(self.append(item)) for item in menu_items]

        self.clear_all_widget.connect("activate", self.on_clear_all_clicked)
        self.add_reminder_widget.connect("activate", self.on_add_reminder_clicked)

    @staticmethod
    def on_add_reminder_clicked(widget):
        windows.open_add_reminder()

    @staticmethod
    def on_clear_all_clicked(widget):
        dbc.remove_all_notifications()


class MailSubMenu(BaseSubMenu):
    def __init__(self):
        add_plugin()
        super(MailSubMenu, self).__init__(self.__class__.__name__, "EMail")
        menu_items = [Gtk.MenuItem("Username/Password")]

        for it in menu_items:
            it.show()

        self.set_credentials_widget = menu_items[0]

        [(self.append(item)) for item in menu_items]

        self.set_credentials_widget.connect("activate", self.on_set_credentials_clicked)

    def on_set_credentials_clicked(self, widget):
        windows.open_set_credentials()


class ConkySubMenu(BaseSubMenu):

    def __init__(self):
        add_plugin()
        super(ConkySubMenu, self).__init__(self.__class__.__name__, "Conky")
        menu_items = [Gtk.MenuItem("Set Color"),
                      Gtk.MenuItem("Display Settings")]

        for it in menu_items:
            it.show()

        self.set_color_widget = menu_items[0]
        self.display_settings_widget = menu_items[1]

        [(self.append(item)) for item in menu_items]

        self.set_color_widget.connect("activate", self.on_set_color_clicked)
        self.display_settings_widget.connect("activate", self.on_display_settings_clicked)

    def on_set_color_clicked(self):
        #ToDo implement on_set_color_clicked
        raise NotImplementedError

    def on_display_settings_clicked(self):
        #ToDo implement on_set_color_clicked
        raise NotImplementedError


