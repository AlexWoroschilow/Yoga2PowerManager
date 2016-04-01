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
import glob
import os.path
import sys
sys.path.append(os.path.dirname(__file__))
import interface


class Pci(interface.Hardware):
    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                if 'auto' not in self._run("cat %s" % device):
                    return False
        return True

    @property
    def devices(self):
        for path in glob.glob("/sys/bus/pci/devices/0000:*"):
            if os.path.exists(path):
                yield "%s/power/control" % path

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo 'auto' > '%s';" % device

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo 'on' > '%s';" % device

    def __str__(self):
        return "PCI"


if __name__ == "__main__":
    print((Pci()))
    print((Pci()).is_powersave)
    print([str(device) for device in (Pci()).devices])
    print([str(device) for device in (Pci()).powersave()])
    print([str(device) for device in (Pci()).perfomance()])
