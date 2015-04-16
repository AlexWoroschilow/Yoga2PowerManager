import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


class Writeback(Switcher):
    def __init__(self):
        self._devices = ["/proc/sys/vm/dirty_writeback_centisecs"]

    def powersave(self):
        for device in self._devices:
            if os.path.isfile(device):
                (Command("echo '1500' > '%s' " % device)).run()


    def perfomance(self):
        for device in self._devices:
            if os.path.isfile(device):
                (Command("echo '0' > '%s' " % device)).run()
