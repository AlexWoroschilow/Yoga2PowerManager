import dbus, sys
import dbus.service
from dbus.exceptions import DBusException


class UPower(dbus.Interface):
    def __init__(self, bus, service, logger):
        self.__proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.UPower')
        self.__properties = dbus.Interface(self.__proxy, 'org.freedesktop.DBus.Properties')


    """
    Get dbus service object
    needs to do an optimizations
    for all switchers and run programm-wide
    commands and so on
    """
    @property
    def service(self):
        return self.__service


    """
    Check is laptop use a battery-power or an AC-power
    """
    @property
    def is_battery(self):
        if self.__properties is not None:
            return bool(self.__properties.Get('org.freedesktop.UPower', 'OnBattery'))
        return None


    """
    Function to notify service about 
    changed state from some system event
    """
    def state_changed(self, options=None):
        pass
