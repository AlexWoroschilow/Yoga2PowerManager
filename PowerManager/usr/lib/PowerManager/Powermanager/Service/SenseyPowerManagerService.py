__author__ = 'sensey'

import dbus
import dbus.service
from Powermanager import Powermanager as pm


class SenseyPowerManagerService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('org.sensey.PowerManager', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/sensey/PowerManager')
        # Enable power-save
        # mode by default
        self.Powersave()

    @dbus.service.method('org.sensey.PowerManager')
    def Powersave(self, options=None):
        (pm.Powermanager()).process(True)

    @dbus.service.method('org.sensey.PowerManager')
    def Perfomance(self, options=None):
        (pm.Powermanager()).process(False)
