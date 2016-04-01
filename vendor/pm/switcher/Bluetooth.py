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
import sys
import os

sys.path.append(os.path.dirname(__file__))
import interface


class Bluetooth(interface.Hardware):
    @property
    def exists(self):
        for device in self.devices:
            return True
        return False

    @property
    def is_powersave(self):
        for device in self.devices:
            if 'DOWN' not in self._run("hciconfig %s " % device):
                return False
        return True

    @property
    def devices(self):
        string = self._run("hciconfig | grep hci")
        return re.findall("hci\d*", string)

    def powersave(self):
        for device in self.devices:
            yield "hciconfig %s down;" % device

    def perfomance(self):
        for device in self.devices:
            yield "hciconfig %s up;" % device

    def __str__(self):
        return "Bluetooth"


if __name__ == "__main__":
    print((Bluetooth()))
    print((Bluetooth()).is_powersave)
    print([str(device) for device in (Bluetooth()).devices])
    print([str(device) for device in (Bluetooth()).powersave()])
    print([str(device) for device in (Bluetooth()).perfomance()])
