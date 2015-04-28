import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher
import os.path


class Hda(Switcher):
    def __init__(self):
        self._devices = ['/sys/module/snd_hda_intel']

    def powersave(self):
        commands = []
        for device in self._devices:
            device_power_save = '%s/parameters/power_save' % device
            if os.path.isfile(device_power_save):
                commands.append("echo '1' > '%s'" % device_power_save)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            device_power_save = '%s/parameters/power_save' % device
            if os.path.isfile(device_power_save):
                commands.append("echo '0' > '%s'" % device_power_save)
        return commands
