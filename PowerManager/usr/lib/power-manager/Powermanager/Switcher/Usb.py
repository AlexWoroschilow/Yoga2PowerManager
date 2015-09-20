import glob
import os.path


class Usb():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = []

        blacklist = ["touchscreen"]
        for device in glob.glob("/sys/bus/usb/devices/*"):
            product_path = "%s/product" % device
            if os.path.isfile(product_path):
                file = open(product_path, 'r')
                product_name = file.read()
                file.close()
                if product_name.lower().strip() in blacklist:
                    continue

            control_path = "%s/power/control" % device
            if os.path.isfile(control_path):
                self._devices.append(control_path)

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            if os.path.isfile(device):
                self._commands.append("echo 'auto' > '%s';" % device)
        return self._commands

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            if os.path.isfile(device):
                self._commands.append("echo 'on' > '%s';" % device)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "USB powersave mode"