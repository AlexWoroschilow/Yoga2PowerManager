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
import inspect
from vendor.Command.Command import Command
from vendor.Switcher import *
import vendor.Switcher as Switchers
from vendor.EventDispatcher import Event
from application.Service.ContainerAware import ContainerAware


class ServicePowerManager(ContainerAware):
    def __init__(self, container):
        super().__init__(container)

        self._switchers = []
        for (name, module) in inspect.getmembers(Switchers, inspect.ismodule):
            identifier = getattr(module, name)
            self._switchers.append(identifier())

    @property
    def switchers(self):
        return self._switchers

    def on_loaded(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug("[ServicePowerManager] on_loaded")

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_powersafe', self.on_powersafe)
        service_event_dispatcher.addListener('app.on_perfomance', self.on_perfomance)
        pass

    def on_started(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug("[ServicePowerManager] on_started")
        pass

    def on_powersafe(self, event, dispatcher):
        service_logger = self.get("logger")
        service_config = self.get("config")
        service_logger.debug("[ServicePowerManager] on_powersafe")

        for switcher in self.switchers:
            if not service_config.ignored(switcher.name):
                for command in switcher.powersave():
                    service_logger.info("[ServicePowerManager] %s" % command)
                    self._run(command)

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_status_changed', Event())
        pass

    def on_perfomance(self, event, dispatcher):
        service_logger = self.get("logger")
        service_config = self.get("config")
        service_logger.debug("[ServicePowerManager] on_perfomance")

        for switcher in self.switchers:
            if not service_config.ignored(switcher.name):
                for command in switcher.perfomance():
                    service_logger.info("[ServicePowerManager] %s" % command)
                    self._run(command)

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_status_changed', Event())
        pass

    def _run(self, command):
        (Command(command)).run()
