import os
import glob
import os.path


class Pci():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = glob.glob("/sys/bus/pci/devices/0000:*")

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                self._commands.append("echo 'auto' > '%s';" % power_control)
        return self._commands

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                self._commands.append("echo 'on' > '%s';" % power_control)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "PCI powersave mode"
