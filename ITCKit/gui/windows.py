__author__ = 'Kristo Koert'

from ITCKit.utils.tools import UrlChecker
from ITCKit.timetable import ical
from ITCKit.core import datatypes
from gi.repository import Gtk, Gdk, GLib
from datetime import datetime
import threading


class BaseWindow(Gtk.Window, threading.Thread):

    def __init__(self, title=""):
        Gtk.Window.__init__(self, title=title)
        threading.Thread.__init__(self)

    def open_error_window(self, message, text):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    def on_close(self, *kwargs):
        self.destroy()


class SetIcalURLWindow(BaseWindow):

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
            from socket import gaierror
            if isinstance(error_message.args[0], gaierror):
                self.info_label = "No internet connection."
            else:
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
        from ITCKit.db import dbc
        try:
            reminder = datatypes.Reminder(self.name_entry.get_text(), self.date_entry.get_text())
            dbc.add_to_db(reminder)
            self._info_label = "Reminder added."
        except ValueError:
            self._info_label = "Invalid datetime."


class SetCredentialsWindow(BaseWindow):

    def __init__(self):
        BaseWindow.__init__(self, title="Set Credentials")
        self.set_size_request(100, 100)

        rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        rows.add(row1)
        rows.add(row2)
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

        self.confirm_button = Gtk.Button("Confirm")
        self.confirm_button.connect("clicked", self.on_confirm_clicked)
        row3.pack_start(self.confirm_button, True, True, 1)

    def on_confirm_clicked(self, widget):
        from ITCKit.mail.credential_security import save_to_keyring
        save_to_keyring(self.username_entry.get_text(), self.password_entry.get_text())


def open_set_credentials():
    win = SetCredentialsWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()
    win.start()


def open_update_timetable():
    win = UpdatingTimetableWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()
    win.start()


def open_set_ical_url():
    win = SetIcalURLWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()


def open_add_reminder():
    win = AddReminderWindow()
    win.connect("delete-event", win.on_close)
    win.show_all()

if __name__ == "__main__":
    pass