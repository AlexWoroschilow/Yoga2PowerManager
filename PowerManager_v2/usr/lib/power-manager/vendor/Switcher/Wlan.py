import re
import os

class Wlan():
    def __init__(self):
        pass
            
    """
    Check is all devices, handled by this object
    are in powersave mode, if on of those is not,
    that means that all module is not in powersave mode
    """
    @property
    def is_powersave(self):
        for device in self.devices:
            if 'on' not in self._run("iw dev %s get power_save" % device):
                return False
        return True


    """
    Get list of devices to handle with
    """
    @property
    def devices(self):
        devices = self._run("ip link show | grep wlan")
        return re.findall("wlan\d*", devices)


    """
    Switch to powersave mode all devices,
    handled by this object, this method already 
    should return just a list with shell commands
    """
    def powersave(self):
        commands = []
        for device in self.devices:
            commands.append("iw dev %s set power_save on" % device)
        return commands


    """
    Enable perfomance mode of devices, 
    handled by this object, this method already should 
    return just a list of shell commands
    """
    def perfomance(self):
        commands = []
        for device in self.devices:
            commands.append("iw dev %s set power_save off" % device)
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
        return "Wlan powersave mode"
    

if __name__ == "__main__":
    print((Wlan()).devices, (Wlan()).is_powersave)
    print((Wlan()).powersave())
    print((Wlan()).perfomance())
