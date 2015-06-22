import dbus
import logging
import dbus.service
from Powermanager.Service.Client.NetworkManager import NetworkManager
from Powermanager.Service.Client.UPower import UPower


class SenseyPowerManagerService(dbus.service.Object):
    """ Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer"""

    def __init__(self, powermanager, logger):
        self.__name = 'org.sensey.PowerManager'
        self.__logger = logger
        self.__power_manager = powermanager
        self.__bus = dbus.SystemBus()
        self.__bus_name = dbus.service.BusName(self.name, self.__bus)

        self.__upower = UPower(self.__bus, self)
        self.__network_manager = NetworkManager(self.__bus, self)

        dbus.service.Object.__init__(self, self.__bus_name, "/" + self.name.replace('.', '/'))

        self.logger.info('start')

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
