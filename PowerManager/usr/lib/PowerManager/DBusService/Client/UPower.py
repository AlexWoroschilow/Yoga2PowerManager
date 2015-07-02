import dbus, sys
import dbus.service
from dbus.exceptions import DBusException


class UPower(dbus.Interface):
    def __init__(self, bus, service, logger):
        self.__logger = logger

        try:
            self.__proxy = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
            dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.UPower')
            self.__properties = dbus.Interface(self.__proxy, 'org.freedesktop.DBus.Properties')

        except DBusException:
            self.logger.critical(sys.exc_info())

    @property
    def logger(self):
        return self.__logger

    def is_battery(self):
        if self.__properties is not None:
            return bool(self.__properties.Get('org.freedesktop.UPower', 'OnBattery'))
        return True