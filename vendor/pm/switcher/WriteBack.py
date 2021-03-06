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
import os.path
import glob
import sys

sys.path.append(os.path.dirname(__file__))
import interface


class WriteBack(interface.Hardware):
    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                if '1500' not in self._run("cat %s" % device):
                    return False
        return True

    @property
    def devices(self):
        for path in glob.glob("/proc/sys/vm/dirty_writeback_centisecs*"):
            if os.path.exists(path):
                yield path

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo '1500' > '%s';" % device

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(device):
                yield "echo '0' > '%s';" % device

    def __str__(self):
        return "Write-Back"


if __name__ == "__main__":
    print((WriteBack()))
    print((WriteBack()).is_powersave)
    print([str(device) for device in (WriteBack()).devices])
    print([str(device) for device in (WriteBack()).powersave()])
    print([str(device) for device in (WriteBack()).perfomance()])
