import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


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