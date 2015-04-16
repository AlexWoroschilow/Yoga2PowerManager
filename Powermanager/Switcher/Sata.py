import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


class Sata(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/class/scsi_host/host*")

    def powersave(self):
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                (Command("/bin/echo 'min_power' > '%s' " % power_control)).run()


    def perfomance(self):
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                (Command("/bin/echo 'medium_power' > '%s' " % power_control)).run()