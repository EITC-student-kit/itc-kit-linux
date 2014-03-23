__author__ = 'Kristo Koert'

from ITCKit.utils.tools import UrlChecker
from ITCKit.timetable import ical

class BaseWindow(Gtk.Window):

    def __init__(self, title=""):
        Gtk.Window.__init__(self, title=title)
        #GLib.timeout_add(10, self.handler_timeout)

    def open_error_window(self, message, text):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()


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
        row2.pack_start(self._info_label, False, False, 10)

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

    _is_updating = True
    info_label = "Updating"

    def __init__(self):
        BaseWindow.__init__(self, title="Update Timetable")
        self.set_size_request(225, 0)

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

        self.update()

        GLib.timeout_add(10, self.handler_timeout)

    def update(self):
        ical.ICalsUpdater(self).start()

    def handler_timeout(self):
        self.checking_animation()
        self._info_label.set_label(self.info_label)
        if self._is_updating:
            self.ok_button.hide()
        else:
            self.ok_button.show()
        return True

    def on_ok_clicked(self, widget):
        self.destroy()

    def checking_animation(self):
        if self._is_updating:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)


def open_update_timetable():
    win = UpdatingTimetableWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()


def open_set_ical_url():
    win = SetIcalURLWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()


if __name__ == "__main__":
    pass