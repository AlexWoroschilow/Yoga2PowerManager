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
import dbus, sys
import dbus.service
from dbus.exceptions import DBusException


class UPower(dbus.Interface):
    def __init__(self, bus, service, logger):
        self.__service = service
        self.__proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.UPower')
        self.__properties = dbus.Interface(self.__proxy, 'org.freedesktop.DBus.Properties')

    @property
    def service(self):
        return self.__service

    @property
    def is_battery(self):
        if self.__properties is not None:
            return bool(self.__properties.Get('org.freedesktop.UPower', 'OnBattery'))
        return None

    def state_changed(self, options=None):
        """
        Function to notify service about
        changed state from some system event
        """
        pass
