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
import sys

sys.path.append(os.path.dirname(__file__))
import interface


class WebCam(interface.Hardware):
    @property
    def exists(self):
        return True

    @property
    def is_powersave(self):
        for device in self.devices:
            if len(self._run("lsmod | grep %s" % device)) > 0:
                return False
        return True

    @property
    def devices(self):
        return ["uvcvideo"]

    def powersave(self):
        for device in self.devices:
            yield "modprobe -r %s;" % device

    def perfomance(self):
        for device in self.devices:
            yield "modprobe %s;" % device

    def __str__(self):
        return "Web camera"


if __name__ == "__main__":
    print((WebCam()))
    print((WebCam()).is_powersave)
    print([str(device) for device in (WebCam()).devices])
    print([str(device) for device in (WebCam()).powersave()])
    print([str(device) for device in (WebCam()).perfomance()])
