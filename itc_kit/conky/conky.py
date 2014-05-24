__author__ = 'Kristo Koert'

import subprocess
from itc_kit.settings.settings import get_timetable_settings
from threading import Thread
from time import sleep
from os import getenv


class Conky(Thread):
    """
    This class deals with running and stopping conky processes.

    This is done by running sub processes for starting them and using the command "killall conky" to stop them.
    Commands are in the format "sh path/to/Start_Conky.sh"
    """
    #ToDo Implement a way to stop conky without killing all instances of conky.

    def __init__(self):
        super(Conky, self).__init__()
        self.process = None
        self.cmd = getenv("HOME") + "/.itc-kit/conky/Start_Conky.sh"

    def run(self):
        while True:
            if get_timetable_settings()["activated"]:
                if self.process is None:
                    self.process = subprocess.Popen(args=self.cmd)
                sleep(1)
            else:
                if self.process is not None:
                    subprocess.call(args="killall conky", shell=True)
                    self.process.terminate()
                    self.process = None
                sleep(1)