import os
import os.path


class Hda():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = ['/sys/module/snd_hda_intel']

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            device_power_save = '%s/parameters/power_save' % device
            if os.path.isfile(device_power_save):
                self._commands.append("echo '1' > '%s';" % device_power_save)
        return self._commands

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            device_power_save = '%s/parameters/power_save' % device
            if os.path.isfile(device_power_save):
                self._commands.append("echo '0' > '%s';" % device_power_save)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "Intel HDA powersave mode"
