__author__ = 'Kristo Koert'

from itc_kit.utils.tools import UrlChecker
from itc_kit.timetable import ical
from itc_kit.core import datatypes
from gi.repository import Gtk, Gdk, GLib
from datetime import datetime


class BaseWindow(Gtk.Window):
    """
    Classes inheriting this are meant to be used as popup windows for task not possible to conduct in the menus.
    """

    def __init__(self, title=""):
        Gtk.Window.__init__(self, title=title)

    def open_error_window(self, message, text):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    def on_close(self, *kwargs):
        self.destroy()


class CustomizeTimetableWindow(BaseWindow):
    """
    Class not implemented
    """
    #ToDo implement CustomizeTimetableWindow

    def __init__(self):
        BaseWindow.__init__(self, title="Set ical URL")
        self.set_size_request(500, 500)

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        rows.add(row1)
        rows.add(row2)
        rows.add(row3)

        self.add(rows)

        confirm_button = Gtk.Button("Confirm")
        #confirm_button.connect("clicked", self.on_verify_clicked)
        row3.pack_start(confirm_button, True, True, 1)

        reset_button = Gtk.Button("Reset")
        #confirm_button.connect("clicked", self.on_verify_clicked)
        row3.pack_start(reset_button, True, True, 1)

        cancel_button = Gtk.Button("Cancel")
        #confirm_button.connect("clicked", self.on_verify_clicked)
        row3.pack_start(cancel_button, True, True, 1)

        confirm_button = Gtk.Button("Search")
        #confirm_button.connect("clicked", self.on_verify_clicked)
        row1.pack_end(confirm_button, True, True, 1)

        self.search_field = Gtk.Entry()
        self.search_field.set_text("Search for class")
        row1.pack_start(self.search_field, True, True, 10)


class SetIcalURLWindow(BaseWindow):
    """
    This class does what it's name implies.

    It is of note that the url verification might not be fool proof.
    """

    _is_checking_url = False
    info_label = "Tip: Log into OIS -> My Schedule -> iCal"

    def __init__(self):
        BaseWindow.__init__(self, title="Set ical URL")
        self.set_size_request(250, 100)

        self.timeout_id = None

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        row4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        rows.add(row1)
        rows.add(row2)
        rows.add(row3)
        rows.add(row4)

        self.add(rows)

        url_label = Gtk.Label("URL: ")
        row1.pack_start(url_label, True, True, 10)

        self.entry = Gtk.Entry()
        self.entry.set_text("The url for your iCal")
        row1.pack_end(self.entry, True, True, 10)

        self._info_label = Gtk.Label("Tip: Log into OIS -> My Schedule -> iCal")
        row2.pack_start(self._info_label, True, True, 10)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_pulse_step(0.01)
        row4.pack_start(self.progressbar, True, True, 0)

        ok_button = Gtk.Button("Verify")
        ok_button.connect("clicked", self.on_verify_clicked)
        row3.pack_start(ok_button, True, True, 1)

        ok_button = Gtk.Button("Exit")
        ok_button.connect("clicked", self.on_exit_clicked)
        row3.pack_end(ok_button, True, True, 1)

        GLib.timeout_add(10, self.handler_timeout)

    def handler_timeout(self):
        self.checking_animation()
        self._info_label.set_label(self.info_label)
        return True

    def on_verify_clicked(self, widget):
        self.info_label = "Verifying URL.."
        UrlChecker(self).start()

    def on_exit_clicked(self, widget):
        self.destroy()

    def checking_animation(self):
        if self._is_checking_url:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)


class UpdatingTimetableWindow(BaseWindow):
    """
    This class opens a window that runs the underling processes that download the ical file at the url specified in the
    settings ical file.

    It is of note that the error messages displayed in the window when something goes awry are exceptions thrown in the
    timetable module.
    """

    _has_updated = False
    info_label = "Updating.."

    def __init__(self):
        BaseWindow.__init__(self, title="Update Timetable")
        self.set_size_request(100, 0)

        self.timeout_id = None

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        rows.add(row1)
        rows.add(row2)
        rows.add(row3)

        self.add(rows)

        self._info_label = Gtk.Label("")
        row1.pack_start(self._info_label, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_pulse_step(0.01)
        row2.pack_start(self.progressbar, True, True, 0)

        self.ok_button = Gtk.Button("Ok")
        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.ok_button.hide()
        row3.pack_start(self.ok_button, True, True, 1)

        GLib.timeout_add(10, self.handler_timeout)

    def run(self):
        self.info_label = "Updating.."
        try:
            ical.update_icals()
            self.info_label = "Done updating!"
        except Exception as error_message:
            #ToDo Does it have to be the first element of the error message?
            from socket import gaierror
            if isinstance(error_message.args[0], gaierror):
                self.info_label = "No internet connection."
            else:
                print(error_message)
                self.info_label = error_message.args[0]
        self._has_updated = True
        return False

    def handler_timeout(self):
        self.checking_animation()
        self._info_label.set_label(self.info_label)
        if self._has_updated:
            self.ok_button.show()
        else:
            self.ok_button.hide()
        return True

    def on_ok_clicked(self, widget):
        self.destroy()

    def checking_animation(self):
        if not self._has_updated:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)


class AddReminderWindow(BaseWindow):
    """
    This class opens a window where reminders can be added.
    """
    _info_label = ""

    def __init__(self):
        BaseWindow.__init__(self, title="Add reminders")
        self.set_size_request(100, 100)

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        rows.add(row1)
        rows.add(row2)
        rows.add(row3)
        rows.add(row4)

        self.add(rows)

        self.name_label = Gtk.Label("Name")
        row1.pack_start(self.name_label, True, True, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text("")
        row1.pack_end(self.name_entry, True, True, 10)

        self.date_label = Gtk.Label("DateTime")
        row2.pack_start(self.date_label, True, True, 0)

        self.date_entry = Gtk.Entry()
        self.date_entry.set_text(datetime.now().__str__()[:16])
        row2.pack_end(self.date_entry, True, True, 10)

        self.info_label = Gtk.Label(self._info_label)
        row3.pack_start(self.info_label, True, True, 0)

        self.add_reminder_button = Gtk.Button("Add Reminder")
        self.add_reminder_button.connect("clicked", self.on_add_reminder_clicked)
        row4.pack_start(self.add_reminder_button, True, True, 1)

        GLib.timeout_add(10, self.handler_timeout)

    def handler_timeout(self):
        self.info_label.set_label(self._info_label)
        return True

    def on_add_reminder_clicked(self, widget):
        from itc_kit.db import dbc
        try:
            reminder = datatypes.Reminder(self.name_entry.get_text(), self.date_entry.get_text())
            dbc.add_to_db(reminder)
            self._info_label = "Reminder added."
        except ValueError:
            self._info_label = "Invalid datetime."


class SetCredentialsWindow(BaseWindow):
    """
    Simple window that allows the user to enter a username and password and save those in a keyring.

    Note: Currently does not conduct a validity check of the credentials which can result in problems.
    """

    def __init__(self):
        BaseWindow.__init__(self, title="Set Credentials")
        self.set_size_request(100, 100)

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        rowW = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        rows.add(row1)
        rows.add(row2)
        rows.add(rowW)
        rows.add(row3)

        self.add(rows)

        self.name_label = Gtk.Label("Username")
        row1.pack_start(self.name_label, True, True, 0)

        self.username_entry = Gtk.Entry()
        self.username_entry.set_text("itcollege username")
        row1.pack_end(self.username_entry, True, True, 10)

        self.date_label = Gtk.Label("Password")
        row2.pack_start(self.date_label, True, True, 0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        row2.pack_end(self.password_entry, True, True, 10)

        self.warning_label = Gtk.Label("For the change to take effect, please restart the app.")
        rowW.pack_start(self.warning_label, True, True, 1)
        self.confirm_button = Gtk.Button("Confirm")

        self.confirm_button.connect("clicked", self.on_confirm_clicked)
        row3.pack_start(self.confirm_button, True, True, 1)

    def on_confirm_clicked(self, widget):
        from itc_kit.mail.password_retention import save_to_keyring
        #ToDo implement a username, password validity check
        save_to_keyring(self.username_entry.get_text(), self.password_entry.get_text())
        self.destroy()


def open_set_credentials():
    win = SetCredentialsWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()


def open_update_timetable():
    win = UpdatingTimetableWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()


def open_set_ical_url():
    win = SetIcalURLWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()


def open_add_reminder():
    win = AddReminderWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()


def open_customize_timetable():
    win = CustomizeTimetableWindow()
    win.connect('delete-event', win.on_close)
    win.show_all()

