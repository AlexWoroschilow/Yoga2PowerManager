import logging
import dbus
import dbus.service

from DBusService.Client.UPower import UPower
from DBusService.Client.NetworkManager import NetworkManager
from Powermanager.Powermanager import Powermanager


class PowerManagerService(dbus.service.Object):
    """ Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer"""

    def __init__(self, name, filename, level):
        self.__name = name
        self.__logger = logging.getLogger(name)
        logging.basicConfig(level=level, filename=filename)

        self.__power_manager = Powermanager(self.logger)
        self.__bus = dbus.SystemBus()
        self.__bus_name = dbus.service.BusName(self.name, self.__bus)

        self.__upower = UPower(self.__bus, self, self.logger)
        self.__network_manager = NetworkManager(self.__bus, self, self.logger)

        dbus.service.Object.__init__(self, self.__bus_name, "/" + self.name.replace('.', '/'))

    @property
    def name(self):
        return self.__name

    @property
    def logger(self):
        return self.__logger

    @property
    def power_manager(self):
        return self.__power_manager

    @dbus.service.method('org.sensey.PowerManager')
    def Optimize(self, options=None):
        if self.__upower.is_battery():
            return self.Powersave(options)
        return self.Perfomance(options)

    @dbus.service.method('org.sensey.PowerManager')
    def Powersave(self, options):
        self.power_manager.powersave()

    @dbus.service.method('org.sensey.PowerManager')
    def Perfomance(self, options):
        self.power_manager.perfomance()
