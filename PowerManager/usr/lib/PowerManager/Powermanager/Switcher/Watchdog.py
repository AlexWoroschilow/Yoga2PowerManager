import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path


class Watchdog(Switcher):
    def __init__(self):
        self._devices = ["/proc/sys/kernel/nmi_watchdog"]

    def powersave(self):
        commands = []
        for device in self._devices:
            if os.path.isfile(device):
                commands.append("echo '0' > '%s' " % device)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            if os.path.isfile(device):
                commands.append("echo '1' > '%s' " % device)
        return commands
