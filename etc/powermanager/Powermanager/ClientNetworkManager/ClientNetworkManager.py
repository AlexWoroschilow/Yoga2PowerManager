__author__ = 'sensey'

import dbus
import dbus.service


class ClientNetworkManager(dbus.Interface):
    def __init__(self, object, dbus_interface, service):
        dbus.Interface.__init__(self, object, dbus_interface)
        self.connect_to_signal("PropertiesChanged", service.Powersave)
