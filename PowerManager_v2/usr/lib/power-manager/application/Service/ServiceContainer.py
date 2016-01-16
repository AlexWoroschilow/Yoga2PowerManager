# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from vendor import Inject
from vendor.EventDispatcher import EventDispatcher

from application.Service.ServiceDBusInterface import ServiceDBusInterface
from application.Service.ServicePowerManager import ServicePowerManager
from application.Service.ServiceLogger import ServiceLogger
from application.Service.ServiceConfig import ServiceConfig


class ServiceContainer(object):
    def __init__(self):
        Inject.configure_once(self.__load)
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_loaded', self.__on_loaded)
        service_event_dispatcher.addListener('app.on_started', self.__on_started)
        pass

    def __load(self, binder):
        binder.bind("logger", ServiceLogger())
        binder.bind("config", ServiceConfig(self))
        binder.bind("event_dispatcher", EventDispatcher())
        binder.bind("dubs_interface", ServiceDBusInterface(self))
        binder.bind("power_manager", ServicePowerManager(self))

    def __on_loaded(self, event, dispatcher):
        service_config = self.get("config")
        service_power_manager = self.get("power_manager")
        service_event_dispatcher = self.get("event_dispatcher")
        service_dubs_interface = self.get("dubs_interface")
        service_logger = self.get("logger")

        service_event_dispatcher.addListener('app.on_loaded', service_logger.on_loaded, 1)
        service_event_dispatcher.addListener('app.on_loaded', service_power_manager.on_loaded, 1)
        service_event_dispatcher.addListener('app.on_loaded', service_dubs_interface.on_loaded, 1)
        service_event_dispatcher.addListener('app.on_loaded', service_config.on_loaded, 0)

    def __on_started(self, event, dispatcher):
        service_config = self.get("config")
        service_power_manager = self.get("power_manager")
        service_event_dispatcher = self.get("event_dispatcher")
        service_dbus_interface = self.get("dubs_interface")
        service_logger = self.get("logger")

        service_event_dispatcher.addListener('app.on_started', service_logger.on_started, 1)
        service_event_dispatcher.addListener('app.on_started', service_power_manager.on_started, 1)
        service_event_dispatcher.addListener('app.on_started', service_dbus_interface.on_started, 1)
        service_event_dispatcher.addListener('app.on_started', service_config.on_started, 0)

    def get(self, name):
        return Inject.instance(name)
