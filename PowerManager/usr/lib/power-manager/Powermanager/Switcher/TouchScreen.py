import glob
import os.path
from Powermanager.Switcher.Usb import Usb


class TouchScreen(Usb):
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = []

        whitelist = ["touchscreen"]
        for device in glob.glob("/sys/bus/usb/devices/*"):
            product_path = "%s/product" % device
            if os.path.isfile(product_path):
                file = open(product_path, 'r')
                product_name = file.read()
                file.close()
                if product_name.lower().strip() in whitelist:
                    control_path = "%s/power/control" % device
                    if os.path.isfile(control_path):
                        self._devices.append(control_path)

    def powersave(self):
        return self._commands


    def __str__(self):
        return "Touch Screen powersave mode"