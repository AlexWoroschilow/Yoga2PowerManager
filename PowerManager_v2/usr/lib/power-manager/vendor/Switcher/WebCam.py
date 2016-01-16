import os


class WebCam(object):
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if len(self._run("lsmod | grep %s" % path_device)) > 0:
                return False
        return True

    @property
    def devices(self):
        return ["uvcvideo"]

    def powersave(self):
        for path_device in self.devices:
            yield "modprobe -r %s;" % path_device

    def perfomance(self):
        for path_device in self.devices:
            yield "modprobe %s;" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "Web camera switcher"


if __name__ == "__main__":
    print((WebCam()))
    print((WebCam()).is_powersave)
    print([str(device) for device in (WebCam()).devices])
    print([str(device) for device in (WebCam()).powersave()])
    print([str(device) for device in (WebCam()).perfomance()])
