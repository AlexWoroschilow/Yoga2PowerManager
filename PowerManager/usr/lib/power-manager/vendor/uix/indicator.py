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
import gi
import gc as garbage
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository.AppIndicator3 import Indicator
from gi.repository.AppIndicator3 import IndicatorCategory
from gi.repository.AppIndicator3 import IndicatorStatus


class IndicatorModuleItem(Gtk.CheckMenuItem):
    _data = None

    def get_module(self):
        """
        This is a getter, is not a common python way
        to create a getter, but it should be
        compatible with Gtk.MenuItem
        coding style
        """
        return self._data

    def set_module(self, value):
        """
        This is a setter, is not a common python way
        to create a getter, but it should be
        compatible with Gtk.MenuItem
        coding style
        """
        self._data = value


class IndicatorLabel(object):
    def __init__(self):
        """
        Get current battery usage state
        recalculate it to Watts
        """
        self._name = None
        with open('/sys/class/power_supply/BAT1/power_now') as file:
            self._name = "%.1f W" % (float(file.readline()) / 1000000)

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self.name


class IndicatorPowerManager(object):
    def __init__(self, dispatcher=None, manager=None):
        self._manager = manager
        self._dispatcher = dispatcher
        self._dispatcher.add_listener('indicator.refresh', self.on_refresh_label)

        self._indicator = Indicator.new(
                "Indicator Power Manager",
                "/usr/share/power-manager/share/icons/1x50px.png",
                IndicatorCategory.SYSTEM_SERVICES
        )
        self._indicator.set_status(IndicatorStatus.ACTIVE)
        self._indicator.set_label(str(IndicatorLabel()), "Indicator Power Manager")
        self._indicator.set_menu(self.menu)

    @property
    def menu(self):
        menu = Gtk.Menu()
        for module in self._manager.modules_available:
            menu.append(self.menu_switcher(module))
        return menu

    @property
    def menu_shutdown(self):
        element = Gtk.MenuItem("Exit")
        element.connect("activate", self.on_shutdown)
        element.show()
        return element

    def menu_switcher(self, module=None):
        element = IndicatorModuleItem(module.label)
        element.set_module(module)
        element.set_active(True if module in self._manager.modules_enabled else False)
        element.connect("activate", self.on_toggle_module)
        element.show()
        return element

    def on_refresh_label(self, event=None, dispatcher=None):
        self._indicator.set_label(str(IndicatorLabel()), "Indicator Power Manager")
        garbage.collect()

    def on_toggle_module(self, item=None):
        module = item.get_module()

        event = self._dispatcher.new_event(module)
        self._dispatcher.dispatch('indicator.module_toggle', event)

        enabled = self._manager.modules_enabled
        item.set_active(True if module in enabled else False)
        garbage.collect()

        return True
