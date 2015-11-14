import re
import os

class WebCam():
    
    """
    Web Camera kernel module switcher
    remove module for powersave mode
    and insert module for perfomance mode
    """
    def __init__(self):
        self._devices = ["uvcvideo"]


    """
    Check is all devices, handled by this object
    are in powersave mode, if on of those is not,
    that means that all module is not in powersave mode
    """
    @property
    def is_powersave(self):
        for device in self.devices:
            string = self._run("lsmod | grep %s" % device)
            if len(string) > 0:
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
        for device in self._devices:
            commands.append("modprobe -r %s" % device)
        return commands


    """
    Enable perfomance mode of devices, 
    handled by this object, this method already should 
    return just a list of shell commands
    """
    def perfomance(self):
        commands = []
        for device in self._devices:
            commands.append("modprobe %s" % device)
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
        return "Web camera kernel module"
    
    
    
if __name__ == "__main__":
    print((WebCam()).devices, (WebCam()).is_powersave)
    print((WebCam()).powersave())
    print((WebCam()).perfomance())
