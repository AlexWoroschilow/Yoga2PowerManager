__author__ = 'sensey'

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

    def __init__(self, bus, powermanager, logger):
        self.__powermanager = powermanager

        self.__proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')

        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.NetworkManager')
        self.connect_to_signal("StateChanged", self.state_changed)


    """
    Method to run an required actions using current energy context
    if network status has been changed
    20 Disconnected,
    30 Disconnecting,
    40 Connecting
    """

    def state_changed(self, options=None):
        if options in [20, 30, 40]:
            self.__powermanager.optimize(options)

