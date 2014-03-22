__author__ = "Kristo Koert"

from threading import Thread
from time import sleep
from datetime import datetime

from ITCKit.core.datatypes import Activity
from ITCKit.db import dbc
from ITCKit.utils import converting


class Stopper(Thread):
    """A thread object that is meant to replicate a stopper. A new instance should be created for tracking another
    activity. This is due to performance considerations.
    """

    def __init__(self, sub_menu, type_of_activity):
        """Initialization uses the super class Thread __init__ function and sets a gtk.PictureMenuItem object to
        be used as a display point for the running stopper time.

        :param sub_menu: Reference to tracking sub-menu instance
        :type sub_menu: TimeManagerSubMenu
        :param type_of_activity: Productive, Neutral, Counterproductive
        :type type_of_activity: str
        """
        super(Stopper, self).__init__()
        self._type_of_activity = type_of_activity
        self.sub_menu_reference = sub_menu
        self._time = 0
        self._exit_thread = False

    def run(self):
        """As long as _exit_thread is false, this objects instance will stay active. When it's true, the instance will
        become inactive and should be left for garbage collection by removing all references to it."""
        start_time = datetime.now()
        while not self._exit_thread:
            self.sub_menu_reference._display_label = converting.sec_to_time(self._time)
            sleep(1)
            self._time += 1
        end_time = datetime.now()
        #ToDo check database writing for Activity. Suspected invalid procedure or value
        new_activity = Activity(self._type_of_activity, start_time, end_time, self._time)
        dbc.add_to_db(new_activity)

    def stop_tracking(self):
        """Lets this thread instance finish. After this all references to this instance should be removed."""
        self._exit_thread = True


if __name__ == "__main__":
    pass