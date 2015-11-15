import json
import sys
import dbus
import dbus.service
from dbus.exceptions import DBusException
import math


class PowerManager(dbus.Interface):
    """ listen a  PropertiesChanged-Event from network-manager
    DBus object  and try to switch to powersave mode
    @todo: do not switch to powersave mode direct, needs to check
    other properties like connected ac adapter and something like this,
    replace Powersave to another Powermanager-enterpoint """

    def __init__(self, bus, app):
        self._proxy = bus.get_object('org.sensey.PowerManager', '/org/sensey/PowerManager')
        dbus.Interface.__init__(self, self._proxy, 'org.sensey.PowerManager')
        self.connect_to_signal("status_changed", app.refresh)


    @property
    def statuses(self):
        return json.loads(self.status(True))


    @property
    def logger(self):
        return self.__logger