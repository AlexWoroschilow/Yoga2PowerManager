import os
import glob
import os.path


class Cpu():
    def __init__(self):
        self._devices = glob.glob("/sys/devices/system/cpu/cpu?")

    """
    Check is all devices, handled by this object
    are in powersave mode, if on of those is not,
    that means that all module is not in powersave mode
    """
    @property
    def is_powersave(self):
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                string = self._run("cat %s" % power_control)
                if 'powersave' not in string :
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
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                commands.append("echo 'powersave' > '%s';" % power_control)
        return commands


    """
    Enable perfomance mode of devices, 
    handled by this object, this method already should 
    return just a list of shell commands
    """
    def perfomance(self):
        commands = []
        for device in self._devices:
            power_control = "%s/cpufreq/scaling_governor" % device
            if os.path.isfile(power_control):
                commands.append("echo 'performance' > '%s';" % power_control)
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
        return "CPU powersave mode"
    
    
if __name__ == "__main__":
    print((Cpu()).devices, (Cpu()).is_powersave)
    print((Cpu()).powersave())
    print((Cpu()).perfomance())
