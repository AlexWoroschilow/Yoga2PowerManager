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
import time
import inspect
from pm.switcher import *
import pm.switcher as Switchers
import subprocess
import threading
from logging import *


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=10):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        self.process.returncode


class PowerManager(object):
    _delay = 1
    _config = None
    _upower = None
    _logger = None

    def __init__(self, config=None, upower=None):
        self._config = config
        self._upower = upower
        self._logger = getLogger('power-manager')

        self._switchers = []
        for (name, module) in inspect.getmembers(Switchers, inspect.ismodule):
            if hasattr(module, name):
                identifier = getattr(module, name)
                with identifier() as switcher:
                    self._logger.debug('loaded: %s' % switcher.name)
                    self._switchers.append(switcher)

        self._config.modules = [module.name for module in self.switchers]

    @property
    def switchers(self):
        for switcher in self._switchers:
            if switcher.exists:
                yield switcher

    @property
    def managed(self):
        for switcher in self.switchers:
            if not self._config.ignored(switcher.name):
                yield switcher

    @property
    def config(self):
        return self._config

    def on_optimize(self, event, dispatcher):
        time.sleep(self._delay)
        if self._upower.is_battery:
            self._logger.info('optimize for battery')
            return self.on_powersafe(event, dispatcher)
        self._logger.info('optimize for ac')
        return self.on_perfomance(event, dispatcher)

    def on_powersafe(self, event, dispatcher):
        for switcher in self.managed:
            self._logger.debug('powersafe: %s' % switcher.name)
            for command in switcher.powersave():
                self._logger.debug('powersafe command: %s' % command)
                self._execute(command)

    def on_perfomance(self, event, dispatcher):
        for switcher in self.managed:
            self._logger.debug('perfomance: %s' % switcher.name)
            for command in switcher.perfomance():
                self._logger.debug('perfomance command: %s' % command)
                self._execute(command)

    @staticmethod
    def _execute(command):
        if command is not None:
            process = Command(command)
            process.run()


class PowerManagerService(object):
    _manager = None

    def __init__(self, config=None, dispatcher=None, upower=None):
        self._manager = PowerManager(config, upower)

        dispatcher.add_listener('power_manager.optimize', self._manager.on_optimize)
        dispatcher.add_listener('power_manager.powersafe', self._manager.on_powersafe)
        dispatcher.add_listener('power_manager.perfomance', self._manager.on_perfomance)
        dispatcher.add_listener('network_manager.optimize', self._manager.on_optimize)

    @property
    def switchers(self):
        return self._manager.switchers

    @property
    def managed(self):
        return self._manager.managed