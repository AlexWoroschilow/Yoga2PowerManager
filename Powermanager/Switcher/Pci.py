import os
from Powermanager.Switcher.Switcher import Switcher
import glob
import os.path

__author__ = 'sensey'


# /usr/sbin/hciconfig hci0 up &> /dev/null &

class Pci(Switcher):
    def __init__(self):
        self._devices = glob.glob("/sys/bus/pci/devices/0000:*:*")

    def powersave(self):
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                os.system("echo 'auto' > '%s' " % power_control)

    def perfomance(self):
        for device in self._devices:
            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                os.system("echo 'on' > '%s' " % power_control)