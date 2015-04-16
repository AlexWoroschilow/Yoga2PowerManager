import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


class Cpu(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/devices/system/cpu/cpu*")

    def powersave(self):
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                (Command("echo 'powersave' > '%s'; " % power_control)).run()

    def perfomance(self):
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                (Command("echo 'performance' > '%s'; " % power_control)).run()