__author__ = 'Kristo Koert'

import subprocess
from itc_kit.settings.settings import get_timetable_settings, get_time_manager_settings
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
        self.table_process = None
        self.rings_process = None
        self.table_cmd = "sh " + getenv("HOME") + '/.itc-kit/conky/Start_Conky.sh "table"'
        self.rings_cmd = "sh " + getenv("HOME") + '/.itc-kit/conky/Start_Conky.sh "rings"'

    def run(self):
        while True:
            self.activate_table()
            self.activate_rings()
            sleep(1)

    def activate_table(self):
        if get_timetable_settings()["activated"]:
            if self.table_process is None:
                self.table_process = subprocess.Popen(args=self.table_cmd, shell=True)
        else:
            if self.table_process is not None:
                self.reset()

    def activate_rings(self):
        if get_time_manager_settings()["activated"]:
            if self.rings_process is None:
                self.rings_process = subprocess.Popen(args=self.rings_cmd, shell=True)
        else:
            if self.rings_process is not None:
                self.reset()

    def reset(self):
        subprocess.call(args="killall conky", shell=True)
        if self.table_process is not None:
            self.table_process.terminate()
        if self.rings_process is not None:
            self.rings_process.terminate()
        self.table_process = None
        self.rings_process = None
