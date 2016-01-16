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
import sys
import dbus
import dbus.service
from dbus.exceptions import DBusException


class NetworkManager(dbus.Interface):
    """
    Listen a  PropertiesChanged-Event from network-manager
    DBus object  and try to switch to powersave mode
    @todo: do not switch to powersave mode direct, needs to check
    other properties like connected ac adapter and something like this,
    replace Powersave to another Powermanager-enterpoint
    """

    def __init__(self, bus, service, logger):
        self.__service = service
        self.__proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.NetworkManager')
        self.connect_to_signal("StateChanged", self.state_changed)

    @property
    def service(self):
        return self.__service

    @property
    def is_battery(self):
        return None

    def state_changed(self, options=None):
        """
        Method to run an required actions using current energy context
        if network status has been changed
        20 Disconnected,
        30 Disconnecting,
        40 Connecting
        """
        if options in [20, 30, 40]:
            self.service.optimize(options)
