__author__ = 'Kristo Koert'

import subprocess
from itc_kit.settings.settings import get_timetable_settings
from threading import Thread
import time
from os import getenv


class Conky(Thread):

    def __init__(self):
        super(Conky, self).__init__()
        self.process = None
        self.cmd = getenv("HOME") + "/.itc-kit/conky/Start_Conky.sh"

    def run(self):
        while True:
            if get_timetable_settings()["activated"]:
                if self.process is None:
                    self.process = subprocess.Popen(args=self.cmd)
                time.sleep(1)
            else:
                if self.process is not None:
                    subprocess.call(args="killall conky", shell=True)
                    self.process.terminate()
                    self.process = None
                time.sleep(1)