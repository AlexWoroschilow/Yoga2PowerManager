import os
import os.path


class WriteBack():
    def __init__(self):
        pass


    """
    Check is all devices, handled by this object
    are in powersave mode, if on of those is not,
    that means that all module is not in powersave mode
    """
    @property
    def is_powersave(self):
        for power_control in self.devices:
            if os.path.isfile(power_control):
                if '1500' not in self._run("cat %s" % power_control):
                    return False
        return True


    """
    Get list of devices to handle with
    """
    @property
    def devices(self):
        return ["/proc/sys/vm/dirty_writeback_centisecs"]


    """
    Switch to powersave mode all devices,
    handled by this object, this method already 
    should return just a list with shell commands
    """
    def powersave(self):
        commands = []
        for device in self.devices:
            if os.path.isfile(device):
                commands.append("echo '1500' > '%s';" % device)
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
                commands.append("echo '0' > '%s';" % device)
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
        return "Dirty writeback optimisations"


    
if __name__ == "__main__":
    print((WriteBack()).devices, (WriteBack()).is_powersave)
    print((WriteBack()).powersave())
    print((WriteBack()).perfomance())
