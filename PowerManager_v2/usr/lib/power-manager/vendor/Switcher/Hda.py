import os
import os.path


class Hda(object):
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                if '1' not in self._run("cat %s" % path_device):
                    return False
        return True

    @property
    def devices(self):
        for path_device in ['/sys/module/snd_hda_intel']:
            yield '%s/parameters/power_save' % path_device

    def powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '1' > '%s';" % path_device

    def perfomance(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '0' > '%s';" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "Intel HDA switcher"


if __name__ == "__main__":
    print((Hda()))
    print((Hda()).is_powersave)
    print([str(device) for device in (Hda()).devices])
    print([str(device) for device in (Hda()).powersave()])
    print([str(device) for device in (Hda()).perfomance()])
