import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path


class Sata(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/class/scsi_host/host*")

    def powersave(self):
        commands = []
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                commands.append("/bin/echo 'min_power' > '%s' " % power_control)
        return commands


    def perfomance(self):
        commands = []
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                commands.append("/bin/echo 'medium_power' > '%s' " % power_control)
        return commands