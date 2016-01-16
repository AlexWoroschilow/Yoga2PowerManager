import glob
import os.path


class Usb(object):
    def __init__(self):
        self._blacklist = ["touchscreen"]

    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                if 'auto' not in device.status:
                    return False
        return True

    @property
    def devices(self):
        for path_device in glob.glob("/sys/bus/usb/devices/*"):
            if os.path.isdir(path_device):
                device = UsbDevice(path_device)
                if os.path.isfile(device.product):
                    if device.name not in self._blacklist:
                        yield device

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'auto' > '%s';" % device.control

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'on' > '%s';" % device.control

    def __str__(self):
        return "USB switcher"


class UsbDevice(object):
    def __init__(self, path):
        self.__path = path
        pass

    @property
    def name(self):
        return self.__content(self.product)
        pass

    @property
    def status(self):
        return self.__content(self.control)
        pass

    @property
    def control(self):
        return "%s/power/control" % self.__path

    @property
    def product(self):
        return "%s/product" % self.__path

    def __content(self, filename):
        string = open(filename, 'r').read()
        if string is not None:
            return string.lower().strip()
        return None

    def __str__(self):
        return str(self.control)


if __name__ == "__main__":
    print((Usb()))
    print((Usb()).is_powersave)
    print([str(device) for device in (Usb()).devices])
    print([str(device) for device in (Usb()).powersave()])
    print([str(device) for device in (Usb()).perfomance()])
