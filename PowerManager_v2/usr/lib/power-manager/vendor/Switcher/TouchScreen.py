import glob
import os.path
from vendor.Switcher.Usb import Usb, UsbDevice


class TouchScreen(Usb):
    def __init__(self):
        self._whitelist = ["touchscreen"]

    @property
    def devices(self):
        for path_device in glob.glob("/sys/bus/usb/devices/*"):
            if os.path.isdir(path_device):
                device = UsbDevice(path_device)
                if os.path.isfile(device.product):
                    if device.name in self._whitelist:
                        yield device
        pass

    def __str__(self):
        return "Touch Screen switcher"
        pass


if __name__ == "__main__":
    print((TouchScreen()))
    print((TouchScreen()).is_powersave)
    print([str(device) for device in (TouchScreen()).devices])
    print([str(device) for device in (TouchScreen()).powersave()])
    print([str(device) for device in (TouchScreen()).perfomance()])
