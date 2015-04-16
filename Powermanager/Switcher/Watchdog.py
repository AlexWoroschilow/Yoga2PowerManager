import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


# echo '1500' > '/proc/sys/vm/dirty_writeback_centisecs'

class Watchdog(Switcher):
    def __init__(self):
        self._devices = ["/proc/sys/kernel/nmi_watchdog"]

    def powersave(self):
        for device in self._devices:
            if os.path.isfile(device):
                os.system("echo '0' > '%s' " % device)

    def perfomance(self):
        for device in self._devices:
            if os.path.isfile(device):
                os.system("echo '1' > '%s' " % device)