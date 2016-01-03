import glob
import os.path


class Usb():
    def __init__(self):
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

            power_control = "%s/power/control" % device
            if os.path.isfile(power_control):
                self._devices.append(power_control)

    """
    Check is all devices, handled by this object
    are in powersave mode, if on of those is not,
    that means that all module is not in powersave mode
    """
    @property
    def is_powersave(self):
        for power_control in self.devices:
            if os.path.isfile(power_control):
                if 'auto' not in self._run("cat %s" % power_control):
                    return False
        return True


    """
    Get list of devices to handle with
    """
    @property
    def devices(self):
        return self._devices
    

    """
    Switch to powersave mode all devices,
    handled by this object, this method already 
    should return just a list with shell commands
    """
    def powersave(self):
        commands = []
        for device in self.devices:
            if os.path.isfile(device):
                commands.append("echo 'auto' > '%s';" % device)
        return commands


    """
    Enable perfomance mode of devices, 
    handled by this object, this method already should 
    return just a list of shell commands
    """
    def perfomance(self):
        commands = []
        for device in self.devices:
            if os.path.isfile(device):
                commands.append("echo 'on' > '%s';" % device)
        return commands


    """
    Run command locally, needs to get statuses of devices 
    and so on, do not use this function to switch device state
    """
    def _run(self, command):
        return os.popen(command).read()


    """
    Get name of current switcher, 
    users can see this names, needs to work with 
    translations for this strings
    """
    def __str__(self):
        return "USB powersave mode"
    
    
if __name__ == "__main__":
    print((Usb()).devices, (Usb()).is_powersave)
    print((Usb()).powersave())
    print((Usb()).perfomance())
