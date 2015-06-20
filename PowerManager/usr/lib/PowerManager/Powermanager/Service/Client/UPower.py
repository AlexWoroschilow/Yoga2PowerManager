__author__ = 'sensey'

import dbus
import dbus.service


class UPower(dbus.Interface):
    def __init__(self, bus, service):
        self.__proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.UPower')
        self.__properties = dbus.Interface(self.__proxy, 'org.freedesktop.DBus.Properties')

    def is_battery(self):
        return bool(self.__properties.Get('org.freedesktop.UPower', 'OnBattery'))