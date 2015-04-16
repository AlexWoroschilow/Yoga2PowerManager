import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


 # echo '0' > '/proc/sys/kernel/nmi_watchdog';

class Sata(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/class/scsi_host/host*")

    def powersave(self):
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                os.system("echo 'min_power' > '%s' " % power_control)

    def perfomance(self):
        for device in self._devices:
            power_control = "%s/link_power_management_policy" % device
            if os.path.isfile(power_control):
                os.system("echo 'medium_power' > '%s' " % power_control)