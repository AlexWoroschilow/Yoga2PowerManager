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

        service_config = self.get("config")
        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            ignored = service_config.ignored(switcher.name)
            print("%15s \t%s" % (switcher, ('ignored' if ignored else 'managed')))

    def status(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] status")

        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            powersafe = switcher.is_powersave
            print("%15s \t%5s" % (switcher, 'powersafe' if powersafe else 'perfomance'))

    def devices(self):
        service_logger = self.get("logger")
        service_logger.debug("[PowerManager] devices")

        service_config = self.get("config")
        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            ignored = service_config.ignored(switcher.name)
            for device in switcher.devices:
                print("%15s, %55s \t%s" % (switcher, str(device), ('ignored' if ignored else 'managed')))
