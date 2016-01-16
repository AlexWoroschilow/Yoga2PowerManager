import os
import glob
import os.path


class Cpu(object):
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                if 'powersave' not in self._run("cat %s" % path_device):
                    return False
        return True

    @property
    def devices(self):
        for path_device in glob.glob("/sys/devices/system/cpu/cpu?"):
            yield "%s/cpufreq/scaling_governor" % path_device

    def powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo 'powersave' > '%s';" % path_device

    def perfomance(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo 'performance' > '%s';" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "CPU switcher"


if __name__ == "__main__":
    print((Cpu()))
    print((Cpu()).is_powersave)
    print([str(device) for device in (Cpu()).devices])
    print([str(device) for device in (Cpu()).powersave()])
    print([str(device) for device in (Cpu()).perfomance()])
