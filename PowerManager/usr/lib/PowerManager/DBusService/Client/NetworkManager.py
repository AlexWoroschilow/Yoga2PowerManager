__author__ = 'sensey'

import sys
import dbus
import dbus.service
from dbus.exceptions import DBusException


class NetworkManager(dbus.Interface):
    """ listen a  PropertiesChanged-Event from network-manager
    DBus object  and try to switch to powersave mode
    @todo: do not switch to powersave mode direct, needs to check
    other properties like connected ac adapter and something like this,
    replace Powersave to another Powermanager-enterpoint """

    def __init__(self, bus, powermanager, logger):
        self.__logger = logger
        self.__powermanager = powermanager

        try:
            self.__proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')

            dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.NetworkManager')
            self.connect_to_signal("StateChanged", self.Optimize)

        except DBusException:
            self.logger.critical(sys.exc_info())

    @property
    def logger(self):
        return self.__logger

    def Optimize(self, options=None):
        if options in [20, 30, 40]:  # Disconnected, Disconnecting, Connecting
            self.__powermanager.Optimize(options)