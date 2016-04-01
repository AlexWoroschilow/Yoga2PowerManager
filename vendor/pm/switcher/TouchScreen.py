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
import sys

sys.path.append(os.path.dirname(__file__))
from Usb import *


class TouchScreen(Usb):
    def __init__(self):
        self._whitelist = ["touchscreen"]

    @property
    def devices(self):
        for path in glob.glob("/sys/bus/usb/devices/*"):
            if os.path.isdir(path):
                device = UsbDevice(path)
                if os.path.isfile(device.product):
                    if device.name in self._whitelist:
                        yield device

    def __str__(self):
        return "Touch Screen"


if __name__ == "__main__":
    print((TouchScreen()))
    print((TouchScreen()).is_powersave)
    print([str(device) for device in (TouchScreen()).devices])
    print([str(device) for device in (TouchScreen()).powersave()])
    print([str(device) for device in (TouchScreen()).perfomance()])
