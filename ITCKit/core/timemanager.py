__author__ = "Kristo Koert"

from threading import Thread
from time import sleep
from datetime import datetime

from ITCKit.core.datatypes import Activity
from ITCKit.db import dbc
from ITCKit.utils import converting


class Stopper(Thread):
    """A thread object that is meant to replicate a stopper. Has the ability to stop temporarily and continue. Though
    a new instance should be created for tracking another activity. This is due to performance considerations.
    """

    def __init__(self, display, type_of_activity):
        """Initialization uses the super class Thread __init__ function and sets a gtk.PictureMenuItem object to
        be used as a display point for the running stopper time.
        :param type_of_activity: Productive, Neutral, Counter-Productive
        :type type_of_activity: str
        :param display: A place to display stopper time
        :type display: Widget
        """
        super(Stopper, self).__init__()
        self._write_to_db = True
        self._type_of_activity = type_of_activity
        self._display = display
        self._time = 0
        self._exit_thread = False

    def run(self):
        """As long as _exit_thread is false, this objects instance will stay active. When it's true, the instance will
        become inactive and should be left for garbage collection by removing all references to it. Toggling _active
        creates a stop and resume effect."""
        start_time = datetime.now()
        while not self._exit_thread:
            self._display = converting.sec_to_time(self._time)
            sleep(1)
            self._time += 1
        if self._write_to_db:
            end_time = datetime.now()
            new_activity = Activity(self._type_of_activity, start_time, end_time, self._time)
            dbc.add_to_db(new_activity)
            self._time = 0

    def stop_tracking(self):
        """Lets this thread instance finish. After this all references to this instance should be removed."""
        self._exit_thread = True

    def reset_tracking(self):
        """Writing to db does not take place."""
        self._write_to_db = False
        self.stop_tracking()

if __name__ == "__main__":
    pass