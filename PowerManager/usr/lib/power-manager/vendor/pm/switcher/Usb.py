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
            return stream.read()\
                .lower().strip()
        return None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        return str(self.control)


class Usb(object):
    def __init__(self):
        """
        Class constructor
        define blacklisted devices by default
        touchscreen are there because it is realy
        complicated to work with touchscreen
        in powersafe mode
        """
        self._blacklist = ["touchscreen"]

    @property
    def name(self):
        """
        Get unique device name to work with
        it is only for objecst and code
        the user should not see it
        """
        return self.__class__\
            .__name__.lower()

    @property
    def is_powersave(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                if 'auto' not in device.status:
                    return False
        return True

    @property
    def devices(self):
        """
        Get list of available devices
        filter by power control posibility
        """
        for device_path in glob.glob("/sys/bus/usb/devices/*"):
            if os.path.isdir(device_path):
                device = UsbDevice(device_path)
                if os.path.isfile(str(device)):
                    if device.name not in self._blacklist:
                        yield device

    def powersave(self):
        """
        Get cmd lines to optimize powr usage
        for given devices
        """
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'auto' > '%s';" % str(device)

    def perfomance(self):
        for device in self.devices:
            if os.path.isfile(str(device)):
                yield "echo 'on' > '%s';" % str(device)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        return "USB"


if __name__ == "__main__":
    print((Usb()))
    print((Usb()).is_powersave)
    print([str(device) for device in (Usb()).powersave()])
    print([str(device) for device in (Usb()).perfomance()])
    for device in (Usb()).devices:
        print(str(device))
