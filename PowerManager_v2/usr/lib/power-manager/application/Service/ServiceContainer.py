'''
Created on 03.01.2016

@author: sensey
'''
from vendor import Inject
from vendor.EventDispatcher import EventDispatcher

from application.Service.ServiceDBusInterface import ServiceDBusInterface
from application.Service.ServicePowerManager import ServicePowerManager
from application.Service.ServiceLogger import ServiceLogger

class ServiceContainer():
    def __init__(self):
        Inject.configure_once(self.__load)
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_loaded', self.__on_loaded)
        service_event_dispatcher.addListener('app.on_started', self.__on_started)
        pass

    def __load(self, binder):
        binder.bind("event_dispatcher", EventDispatcher())
        binder.bind("dubs_interface", ServiceDBusInterface(self))
        binder.bind("power_manager", ServicePowerManager(self))

        pass

    def __on_loaded(self, event, dispatcher):
        service_power_manager = self.get("power_manager")
        service_dubs_interface = self.get("dubs_interface")
        service_event_dispatcher = self.get("event_dispatcher")

        service_event_dispatcher.addListener('app.on_loaded', service_power_manager.on_loaded)
        service_event_dispatcher.addListener('app.on_loaded', service_dubs_interface.on_loaded)
        pass

    def __on_started(self, event, dispatcher):
        service_power_manager = self.get("power_manager")
        service_dubs_interface = self.get("dubs_interface")
        service_event_dispatcher = self.get("event_dispatcher")

        service_event_dispatcher.addListener('app.on_started', service_power_manager.on_started)
        service_event_dispatcher.addListener('app.on_started', service_dubs_interface.on_started)
        pass

    def get(self, name):
        return Inject.instance(name)
        pass
        
