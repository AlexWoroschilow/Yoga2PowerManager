import sys
from dbus import DBusException
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

from application.Service.ServiceContainer import ServiceContainer
from vendor import Inject
from vendor.EventDispatcher import Event

class PowerManager():
    def __init__(self):
        self.container = ServiceContainer()
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_loaded', Event())
        pass
    
    """
    Show all available and enabled modules
    for current power manager context
    """
    def start(self):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_started', Event())
        pass

    def powersave(self):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_powersafe', Event())
        pass

    def perfomance(self):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_perfomance', Event())
        pass

    """
    Show all available and enabled modules
    for current power manager context
    """
    def modules(self):
        for switcher in self.container.get("power_manager").switchers:
            print("Module:\t%10s" % (switcher))
        pass

    """
    Show all current power states over module
    for current power manager context
    """
    def status(self):
        for switcher in self.container.get("power_manager").switchers:
            print("Module:\t%10s, \tPowersave: %5s" % (switcher, switcher.is_powersave))
        pass

    """
    Show all available devices
    for current power manager context
    """
    def devices(self):
        for switcher in self.container.get("power_manager").switchers:
            for device in switcher.devices:
                print("Module:\t%10s, Device: %40s" % (switcher, device))
        pass
