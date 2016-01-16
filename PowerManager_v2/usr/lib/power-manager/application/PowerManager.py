import sys
from dbus import DBusException
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

from application.Service.ContainerAware import ContainerAware
from application.Service.ServiceContainer import ServiceContainer
from vendor import Inject
from vendor.EventDispatcher import Event


class PowerManager(ContainerAware):
    def __init__(self):
        super().__init__(ServiceContainer())
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_loaded', Event())

    def start(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] start")

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_started', Event())

    def powersave(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] powersave")

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_powersafe', Event())

    def perfomance(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] perfomance")

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_perfomance', Event())

    def modules(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] modules")

        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            print("Module:\t%10s" % (switcher))

    def status(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] status")

        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            print("Powersave: %5s\t %10s" % (switcher.is_powersave, switcher))

    def devices(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] devices")

        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            for device in switcher.devices:
                print("Module:\t%10s, Device: %40s" % (switcher, str(device)))
