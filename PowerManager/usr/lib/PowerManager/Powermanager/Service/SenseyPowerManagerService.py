__author__ = 'sensey'

import dbus
import dbus.service
from Powermanager.Service.Client.NetworkManager import NetworkManager
from Powermanager.Service.Client.UPower import UPower


class SenseyPowerManagerService(dbus.service.Object):
    """ Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer"""

    def __init__(self, powermanager):
        self.__bus = dbus.SystemBus()
        self.__bus_name = dbus.service.BusName('org.sensey.PowerManager', self.__bus)

        self.__upower = UPower(self.__bus, self)
        self.__network_manager = NetworkManager(self.__bus, self)
        self.__power_manager = powermanager

        dbus.service.Object.__init__(self, self.__bus_name, '/org/sensey/PowerManager')


    @dbus.service.method('org.sensey.PowerManager')
    def Optimize(self, options=None):
        if self.__upower.is_battery():
            return self.Powersave(options)
        return self.Perfomance(options)


    @dbus.service.method('org.sensey.PowerManager')
    def Powersave(self, options):
        self.__power_manager.powersave()


    @dbus.service.method('org.sensey.PowerManager')
    def Perfomance(self, options):
        self.__power_manager.perfomance()
