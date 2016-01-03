import json
import logging
import dbus
import dbus.service
import inspect
from vendor import Inject
from vendor.EventDispatcher import Event
import sys
from dbus import DBusException
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

from vendor.DBusListeners import *
import vendor.DBusListeners as Clients

class ServiceDBusInterface(dbus.service.Object):
    """
    Start a Powermanager DBus service, with some custom methods
    to switch a current power mode for computer
    """
    def __init__(self, container):
        self.container = container
        pass

    
    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_status_changed', self.on_status_changed)
        pass


    def on_started(self, event, dispatcher):
        DBusGMainLoop(set_as_default=True)
        try:

            bus = dbus.SystemBus()
            self.__listeners = []
            for (name, module) in inspect.getmembers(Clients, inspect.ismodule):
                if hasattr(module, name):
                    identifier = getattr(module, name)
                    self.__listeners.append(identifier(bus, self, None))
    
            dbus.service.Object.__init__(self, dbus.service.BusName("org.sensey.PowerManager", bus), "/org/sensey/PowerManager")

            self.optimize(None)

        except DBusException as exception:
            print(exception.get_dbus_message())
            sys.exit(0)
        (GObject.MainLoop()).run()

        pass


    def on_status_changed(self, event, dispatcher):
        self.status_changed()
        pass


    """
    Get list of all listeners
    which listen a system objects over dbus
    and try to optimize power state with 
    respect to system condition
    """
    @property
    def listeners(self):
        return self.__listeners
        pass

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
        pass


    """
    DBus method to optimize power usage
    with respect to current conditions
    """
    @dbus.service.method('org.sensey.PowerManager')
    def optimize(self, options=None):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_powersafe' if self.is_battery else 'app.on_perfomance', Event())
        pass


    """
    DBus method to run powersave mode
    """
    @dbus.service.method('org.sensey.PowerManager')
    def powersave(self, options):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_powersafe', Event())
        pass


    """
    DBus method to run perfomance mode
    """
    @dbus.service.method('org.sensey.PowerManager')
    def perfomance(self, options):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_perfomance', Event())
        pass


    """
    DBus method to get current status of all modules
    """
    @dbus.service.method('org.sensey.PowerManager')
    def status(self, options):
        response = {}
        for switcher in self.container.get("power_manager").switchers:
            response[switcher.__str__()] = switcher.is_powersave
        return json.dumps(response)
        pass


    """
    DBus signal to notify other
    object about changed status
    """
    @dbus.service.signal(dbus_interface='org.sensey.PowerManager', signature='')
    def status_changed(self):
        pass
