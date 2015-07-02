import glob
import os.path
from Powermanager.Switcher.Switcher import Switcher


class Usb(Switcher):
    def __init__(self):
        self._ignore = ['touchscreen']
        self._devices = glob.glob("/sys/bus/usb/devices/*")

    def powersave(self):
        commands = []
        for device in self._devices:
            device_product = "%s/product" % device
            device_power_control = "%s/power/control" % device
            if os.path.isfile(device_product):
                device_name = open(device_product, 'r')
                name = device_name.read()
                if name.lower().strip() in self._ignore:
                    continue

            if os.path.isfile(device_power_control):
                commands.append("echo 'auto' > '%s' " % device_power_control)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            device_power_control = "%s/power/control" % device
            if os.path.isfile(device_power_control):
                commands.append("echo 'on' > '%s' " % device_power_control)
        return commands