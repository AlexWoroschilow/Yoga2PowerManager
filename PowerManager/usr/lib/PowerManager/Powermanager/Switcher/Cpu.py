import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path


class Cpu(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/devices/system/cpu/cpu*")

    def powersave(self):
        commands = []
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                commands.append("echo 'powersave' > '%s'; " % power_control)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                commands.append("echo 'performance' > '%s'; " % power_control)
        return commands