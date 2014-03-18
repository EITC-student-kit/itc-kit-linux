__author__ = 'Kristo Koert'

#!/usr/bin/python
from gi.repository import Gtk


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ITCKit")

        self.button = Gtk.Button(label="Update Timetable")
        self.button.connect("clicked", self.on_update_timetable_clicked)
        self.add(self.button)

    def on_update_timetable_clicked(self, widget):
        print("Update Timetable process")


def open_main_window():
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
