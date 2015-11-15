import json
import logging
import dbus
import dbus.service
import inspect

from DBusService.Listeners import *
import DBusService.Listeners as Client


class PowerManagerService(dbus.service.Object):
    """
    Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer
    """
    def __init__(self, busname, power_manager, logger):
        self.__power_manager = power_manager

        bus = dbus.SystemBus()

        self.__listeners = []
        for (name, module) in inspect.getmembers(Client, inspect.ismodule):
            if hasattr(module, name):
                identifier = getattr(module, name)
                self.__listeners.append(identifier(bus, self, logger))


        dbus.service.Object.__init__(self, dbus.service.BusName(busname, bus), "/" + busname.replace('.', '/'))


    """
    Get list of all listeners
    which listen a system objects over dbus
    and try to optimize power state with 
    respect to system condition
    """
    @property
    def listeners(self):
        return self.__listeners


    """
    Try to identify is system 
    uses a battery now or AC
    """
    @property
    def is_battery(self):
        for listener in self.listeners:
            is_use_battery = listener.is_battery
            if is_use_battery is not None:
                if not is_use_battery :
                    return False
        return True
            

    """
    DBus method to optimize power usage
    with respect to current conditions
    """
    @dbus.service.method('org.sensey.PowerManager')
    def optimize(self, options=None):
        if self.is_battery :
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
