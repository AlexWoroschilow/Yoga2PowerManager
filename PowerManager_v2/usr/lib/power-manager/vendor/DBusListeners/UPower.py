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
