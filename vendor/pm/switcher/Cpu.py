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


class Cpu(interface.Hardware):
    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                if 'powersave' not in self._run("cat %s" % device):
                    return False
        return True

    @property
    def devices(self):
        for path in glob.glob("/sys/devices/system/cpu/cpu?"):
            if os.path.exists(path):
                yield "%s/cpufreq/scaling_governor" % path

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo 'powersave' > '%s';" % device

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo 'performance' > '%s';" % device

    def __str__(self):
        return "CPU"


if __name__ == "__main__":
    print((Cpu()))
    print((Cpu()).is_powersave)
    print([str(device) for device in (Cpu()).devices])
    print([str(device) for device in (Cpu()).powersave()])
    print([str(device) for device in (Cpu()).perfomance()])
