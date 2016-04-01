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
import glob
import os.path
import sys

sys.path.append(os.path.dirname(__file__))
import interface


class Usb(interface.Hardware):
    def __init__(self):
        self._blacklist = ["touchscreen"]

    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                if 'auto' not in device.status:
                    return False
        return True

    @property
    def devices(self):
        for path in glob.glob("/sys/bus/usb/devices/*"):
            if os.path.isdir(path):
                device = UsbDevice(path)
                if os.path.isfile(str(device)):
                    if device.name not in self._blacklist:
                        yield device

    def powersave(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'auto' > '%s';" % str(device)

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'on' > '%s';" % str(device)

    def __str__(self):
        return "USB"


class UsbDevice(object):
    def __init__(self, path):
        self.__path = path

    @property
    def name(self):
        if os.path.isfile(self.product):
            return self.__content(self.product)
        return "Unknown usb device"

    @property
    def status(self):
        return self.__content(self.control)

    @property
    def control(self):
        return "%s/power/control" % self.__path

    @property
    def product(self):
        return "%s/product" % self.__path

    def __content(self, filename):
        with open(filename, 'r') as stream:
            return stream.read().lower().strip()
        return None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        return str(self.control)


if __name__ == "__main__":
    print((Usb()))
    print((Usb()).is_powersave)
    print([str(device) for device in (Usb()).powersave()])
    print([str(device) for device in (Usb()).perfomance()])
    for device in (Usb()).devices:
        print(str(device))
