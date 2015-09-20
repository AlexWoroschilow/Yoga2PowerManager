import os
import glob
import os.path


class Sata():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = glob.glob("/sys/class/scsi_host/host*")

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                self._commands.append("/bin/echo 'min_power' > '%s';" % power_control)
        return self._commands


    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                self._commands.append("/bin/echo 'medium_power' > '%s';" % power_control)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "SATA powersave mode"