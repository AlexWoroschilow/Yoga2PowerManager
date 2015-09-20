import json
import logging
import dbus
import dbus.service

from DBusService.Client.UPower import UPower
from DBusService.Client.NetworkManager import NetworkManager
from Powermanager.Powermanager import Powermanager


class PowerManagerService(dbus.service.Object):
    """
    Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer
    """

    def __init__(self, name, power_manager, logger):

        bus = dbus.SystemBus()

        self.__upower = UPower(bus, self, logger)
        self.__network_manager = NetworkManager(bus, self, logger)
        self.__power_manager = power_manager

        dbus.service.Object.__init__(self, dbus.service.BusName(name, bus), "/" + name.replace('.', '/'))

    """
    DBus method to optimize power usage
    with respect to current conditions
    """

    @dbus.service.method('org.sensey.PowerManager')
    def optimize(self, options=None):
        if self.__upower.is_battery():
            return self.powersave(options)
        return self.perfomance(options)

    """
    DBus method to run powersave mode
    """

    @dbus.service.method('org.sensey.PowerManager')
    def powersave(self, options):
        self.__power_manager.powersave()
        self.status_changed()

    """
    DBus method to run perfomance mode
    """

    @dbus.service.method('org.sensey.PowerManager')
    def perfomance(self, options):
        self.__power_manager.perfomance()
        self.status_changed()

    """
    DBus method to get current status of all modules
    """

    @dbus.service.method('org.sensey.PowerManager')
    def status(self, options):
        response = {}
        for switcher in self.__power_manager.switchers:
            response[switcher.__str__()] = switcher.is_powersave
        return json.dumps(response)

    """
    DBus signal to notify other
    object about changed status
    """

    @dbus.service.signal(dbus_interface='org.sensey.PowerManager', signature='')
    def status_changed(self):
        pass
