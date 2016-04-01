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
import glob
import os.path

sys.path.append(os.path.dirname(__file__))
import interface


class Apache2(interface.Software):
    @property
    def devices(self):
        for path in glob.glob("/etc/init.d/apache2*"):
            if os.path.isfile(path):
                yield path

    def __str__(self):
        return "Apache2"


if __name__ == "__main__":
    print((Apache2()))
    print((Apache2()).is_powersave)
    print((Apache2()).exists)
    print([str(device) for device in (Apache2()).devices])
    print([str(device) for device in (Apache2()).powersave()])
