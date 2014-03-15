__author__ = "Kristo Koert"

from threading import Thread
from time import sleep

from ITCKit.utils import converting


class Stopper(Thread):
    """A thread object that is meant to replicate a stopper. Has the ability to stop temporarily and continue. Though
    a new instance should be created for tracking another activity. This is due to performance considerations.
    """

    _show_time_in_indicator = True

    def __init__(self, indicator):
        """Initialization uses the super class Thread __init__ function and sets a gtk.PictureMenuItem object to
        be used as a display point for the running stopper time.

        :param indicator: A place to display stopper time
        :type indicator: Indicator
        """
        super(Stopper, self).__init__()
        self._indicator = indicator
        self._time = 0
        self._active = False
        self._exit_thread = False

    def run(self):
        """As long as _exit_thread is false, this objects instance will stay active. When it's true, the instance will
        become inactive and should be left for garbage collection by removing all references to it. Toggling _active
        creates a stop and resume effect."""
        while not self._exit_thread:
            while self._active and not self._exit_thread:
                if self._show_time_in_indicator:
                    self._indicator.set_label(converting.sec_to_time(self._time))
                sleep(1)
                self._time += 1
            while not self._active and not self._exit_thread:
                sleep(1)

    def toggle_active(self):
        self._active = not self._active

    def stop_tracking(self):
        """Lets this thread instance finish. After this all references to this instance should be removed."""
        self._exit_thread = True


if __name__ == "__main__":
    pass
