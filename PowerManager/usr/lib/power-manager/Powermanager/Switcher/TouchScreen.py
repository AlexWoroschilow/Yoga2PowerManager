import glob
import os.path
from Powermanager.Switcher.Usb import Usb


class TouchScreen(Usb):
    def __init__(self):
        self._devices = []

        whitelist = ["touchscreen"]
        for device in glob.glob("/sys/bus/usb/devices/*"):
            product_path = "%s/product" % device
            if os.path.isfile(product_path):
                file = open(product_path, 'r')
                product_name = file.read()
                file.close()
                if product_name.lower().strip() in whitelist:
                    power_control = "%s/power/control" % device
                    if os.path.isfile(power_control):
                        self._devices.append(power_control)


    """
    Switch to powersave mode all devices,
    handled by this object, this method already 
    should return just a list with shell commands
    """
    def powersave(self):
        return []


    """
    Get name of current switcher, 
    users can see this names, needs to work with 
    translations for this strings
    """
    def __str__(self):
        return "Touch Screen powersave mode"


    
if __name__ == "__main__":
    print((TouchScreen()).devices, (TouchScreen()).is_powersave)
    print((TouchScreen()).powersave())
    print((TouchScreen()).perfomance())
