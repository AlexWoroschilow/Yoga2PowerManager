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


class MySQL(interface.Software):
    @property
    def devices(self):
        for path in glob.glob("/etc/init.d/mysql*"):
            if os.path.isfile(path):
                yield path

    def __str__(self):
        return "MySQL"


if __name__ == "__main__":
    print((MySQL()))
    print((MySQL()).is_powersave)
    print((MySQL()).exists)
    print([str(device) for device in (MySQL()).devices])
    print([str(device) for device in (MySQL()).powersave()])
