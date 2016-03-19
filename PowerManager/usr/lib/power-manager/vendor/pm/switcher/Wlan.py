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
import re
import os


class Wlan(object):
    @property
    def name(self):
        return self.__class__\
            .__name__.lower()

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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        return "Wlan"


if __name__ == "__main__":
    print((Wlan()))
    print((Wlan()).is_powersave)
    print([str(device) for device in (Wlan()).devices])
    print([str(device) for device in (Wlan()).powersave()])
    print([str(device) for device in (Wlan()).perfomance()])
