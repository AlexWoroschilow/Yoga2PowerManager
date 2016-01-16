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
from configparser import ConfigParser
from application.Service.ContainerAware import ContainerAware


class ServiceConfig(ContainerAware):
    def __init__(self, container, config="/etc/power-manager/power-manager.cnf"):
        super().__init__(container)
        self._config = config
        self._parser = ConfigParser()
        self._parser.read(self._config)
        pass

    def on_loaded(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug("[ServicePowerManager] on_loaded")

        modules = [module for module in self.__modules()]
        service_logger.info("[ServicePowerManager] modules: %s" % (",").join(modules))

        self._parser.set('general', 'available', (",").join(modules))
        with open(self._config, 'w') as configfile:
            self._parser.write(configfile)
        pass

    def on_started(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug("[ServicePowerManager] on_loaded")
        pass

    def ignored(self, module):
        blacklist = self._parser.get('general', 'ignored')
        if blacklist is not None:
            return True if module in blacklist.split(',') else False
        pass

    def __modules(self):
        service_power_manager = self.get("power_manager")
        for switcher in service_power_manager.switchers:
            yield switcher.name


if __name__ == "__main__":
    print((ServiceConfig(None, "/home/sensey/Projects/PowerManager/PowerManager_v2/usr/lib/power-manager/powermanager.cnf")))