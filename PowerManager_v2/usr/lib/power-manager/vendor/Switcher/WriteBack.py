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


class WriteBack(object):
    def __init__(self):
        pass

    @property
    def is_powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                if '1500' not in self._run("cat %s" % path_device):
                    return False
        return True

    @property
    def devices(self):
        return ["/proc/sys/vm/dirty_writeback_centisecs"]

    def powersave(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '1500' > '%s';" % path_device

    def perfomance(self):
        for path_device in self.devices:
            if os.path.isfile(path_device):
                yield "echo '0' > '%s';" % path_device

    def _run(self, command):
        return os.popen(command).read()

    def __str__(self):
        return "Dirty writeback switcher"


if __name__ == "__main__":
    print((WriteBack()))
    print((WriteBack()).is_powersave)
    print([str(device) for device in (WriteBack()).devices])
    print([str(device) for device in (WriteBack()).powersave()])
    print([str(device) for device in (WriteBack()).perfomance()])
