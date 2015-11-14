import os
import os.path
import re


class Hda():
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
            power_control = '%s/parameters/power_save' % device
            if os.path.isfile(power_control):
                if '1' not in self._run("cat %s" % power_control):
                    return False
        return True


    """
    Get list of devices to handle with
    """
    @property
    def devices(self):
        return ['/sys/module/snd_hda_intel']


    """
    Switch to powersave mode all devices,
    handled by this object, this method already 
    should return just a list with shell commands
    """
    def powersave(self):
        commands = []
        for device in self.devices:
            power_control = '%s/parameters/power_save' % device
            if os.path.isfile(power_control):
                commands.append("echo '1' > '%s';" % power_control)
        return commands


    """
    Enable perfomance mode of devices, 
    handled by this object, this method already should 
    return just a list of shell commands
    """
    def perfomance(self):
        commands = []
        for device in self.devices:
            power_control = '%s/parameters/power_save' % device
            if os.path.isfile(power_control):
                commands.append("echo '0' > '%s';" % power_control)
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
        return "Intel HDA powersave mode"



if __name__ == "__main__":
    print((Hda()).devices, (Hda()).is_powersave)
    print((Hda()).powersave())
    print((Hda()).perfomance())
