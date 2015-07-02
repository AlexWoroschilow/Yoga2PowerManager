import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path


class Pci(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/bus/pci/devices/0000:*")

    def powersave(self):
        commands = []
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                commands.append("echo 'auto' > '%s'; " % power_control)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                commands.append("echo 'on' > '%s'; " % power_control)
        return commands