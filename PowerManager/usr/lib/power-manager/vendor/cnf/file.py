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
import string
from configparser import ConfigParser


class ConfigFileParser(ConfigParser):
    @property
    def available(self):
        collection = self.get('general', 'available')
        if collection.find(',') is not -1:
            return collection.split(',')
        return [collection]

    @available.setter
    def available(self, value):
        available_string = (',').join(value)
        self.set('general', 'available',
                 available_string.strip(' \t\n\r,'))

    @property
    def blacklist(self):
        raw = self.get('general', 'blacklist')

        collection = raw.strip(' \t\n\r,')
        if collection.find(',') is not -1:
            return collection.split(',')
        return [collection]

    @blacklist.setter
    def blacklist(self, value):
        blacklist_string = (',').join(value)
        self.set('general', 'blacklist',
                 blacklist_string.strip(' \t\n\r,'))


class ConfigFile(object):
    def __init__(self, config="power-manager.ini", dispatcher=None, powermanager=None):
        dispatcher.add_listener('network_manager.module_toggle', self.on_module_toggle)
        dispatcher.add_listener('network_manager.module_enable', self.on_module_enable)
        dispatcher.add_listener('network_manager.module_disable', self.on_module_disable)

        self._config = config
        self._parser = ConfigFileParser()
        self._parser.read(self._config)

        self._dispatcher = dispatcher
        self._powermanager = powermanager

    @property
    def modules(self):
        for switcher in self._powermanager.switchers:
            yield switcher.name

    @modules.setter
    def modules(self, value):
        self._parser.available = value
        with open(self._config, 'w') as stream:
            self._parser.write(stream)

    def ignored(self, module=None):
        blacklist = self._parser.blacklist
        if blacklist is None:
            return False

        return True if module in blacklist \
            else False

    def on_module_toggle(self, event, dispatcher):
        module = event.data
        if self.ignored(module.name):
            self.on_module_enable(event, dispatcher)
            return None

        self.on_module_disable(event, dispatcher)
        return None

    def on_module_enable(self, event, dispatcher):
        module = event.data
        blacklist = self._parser.blacklist
        if self.ignored(module.name):
            index = blacklist.index(module.name)
            blacklist.pop(index)
            self._parser.blacklist = blacklist

            with open(self._config, 'w') as stream:
                self._parser.write(stream)
                return None

        return None

    def on_module_disable(self, event, dispatcher):
        module = event.data
        blacklist = self._parser.blacklist
        if not self.ignored(module.name):
            blacklist.append(module.name)
            self._parser.blacklist = blacklist

            with open(self._config, 'w') as stream:
                self._parser.write(stream)
                return None

        return None
