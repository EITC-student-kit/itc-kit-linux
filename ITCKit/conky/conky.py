__author__ = 'Kristo Koert'

import subprocess
from ITCKit.settings.settings import get_timetable_settings, get_conky_settings
from threading import Thread
import time


class Conky(Thread):

    def __init__(self):
        super(Conky, self).__init__()
        self.process = None
        self.cmd = get_conky_settings()["scriptPath"]

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