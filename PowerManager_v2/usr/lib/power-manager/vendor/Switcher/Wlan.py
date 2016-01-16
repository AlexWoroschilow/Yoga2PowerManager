import re
import os


class Wlan(object):
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if 'on' not in self._run("iw dev %s get power_save" % path_device):
                return False
        return True

    @property
    def devices(self):
        return re.findall("wlan\d*", self._run("ip link show | grep wlan"))

    def powersave(self):
        for path_device in self.devices:
            yield "iw dev %s set power_save on;" % path_device

    def perfomance(self):
        for path_device in self.devices:
            yield "iw dev %s set power_save off;" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "Wlan switcher"


if __name__ == "__main__":
    print((Wlan()))
    print((Wlan()).is_powersave)
    print([str(device) for device in (Wlan()).devices])
    print([str(device) for device in (Wlan()).powersave()])
    print([str(device) for device in (Wlan()).perfomance()])
