# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
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
