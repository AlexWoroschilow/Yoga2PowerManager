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

from pm.switcher import *
import pm.switcher as Switchers
import subprocess
import threading


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=10):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        self.process.returncode


class PowerManager(object):
    def __init__(self, config=None, dispatcher=None, upower=None):
        self._config = config
        self._upower = upower

        dispatcher.add_listener('power_manager.optimize', self.on_optimize)
        dispatcher.add_listener('power_manager.powersafe', self.on_powersafe)
        dispatcher.add_listener('power_manager.perfomance', self.on_perfomance)
        dispatcher.add_listener('network_manager.optimize', self.on_optimize)

        self._switchers = []
        for (name, module) in inspect.getmembers(Switchers, inspect.ismodule):
            identifier = getattr(module, name)
            with identifier() as switcher:
                self._switchers.append(switcher)

        self._config.modules = [module.name for module in self.switchers]

    @property
    def switchers(self):
        return self._switchers

    @property
    def managed(self):
        for switcher in self._switchers:
            if not self._config.ignored(switcher.name):
                yield switcher

    @property
    def config(self):
        return self._config

    def on_optimize(self, event, dispatcher):
        if self._upower.is_battery:
            self.on_powersafe(event, dispatcher)
            return None

        self.on_perfomance(event, dispatcher)
        return None

    def on_powersafe(self, event, dispatcher):
        for switcher in self.switchers:
            if not self.config.ignored(switcher.name):
                for command in switcher.powersave():
                    self._run(command)

    def on_perfomance(self, event, dispatcher):
        for switcher in self.switchers:
            if not self.config.ignored(switcher.name):
                for command in switcher.perfomance():
                    self._run(command)

    def _run(self, command):
        process = Command(command)
        process.run()


# if __name__ == "__main__":
#     print(PowerManager())
