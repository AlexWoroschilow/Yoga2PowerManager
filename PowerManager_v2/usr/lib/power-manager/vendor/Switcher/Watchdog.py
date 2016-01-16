import os
import os.path


class Watchdog():
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                if '0' not in self._run("cat %s" % path_device):
                    return False
        return True

    @property
    def devices(self):
        return ["/proc/sys/kernel/nmi_watchdog"]

    def powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '0' > '%s';" % path_device

    def perfomance(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '1' > '%s';" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "Watchdog switcher"


if __name__ == "__main__":
    print((Watchdog()))
    print((Watchdog()).is_powersave)
    print([str(device) for device in (Watchdog()).devices])
    print([str(device) for device in (Watchdog()).powersave()])
    print([str(device) for device in (Watchdog()).perfomance()])
