__author__ = 'sensey'

import dbus
import dbus.service


class NetworkManager(dbus.Interface):
    """ listen a  PropertiesChanged-Event from network-manager
    DBus object  and try to switch to powersave mode
    @todo: do not switch to powersave mode direct, needs to check
    other properties like connected ac adapter and something like this,
    replace Powersave to another Powermanager-enterpoint """

    def __init__(self, bus, powermanager):
        self.__powermanager = powermanager
        self.__proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')

        dbus.Interface.__init__(self, self.__proxy, 'org.freedesktop.NetworkManager')
        self.connect_to_signal("StateChanged", self.Optimize)

    def Optimize(self, options=None):
        if options in [20, 30, 40]:  # Disconnected, Disconnecting, Connecting
            self.__powermanager.Optimize(options)