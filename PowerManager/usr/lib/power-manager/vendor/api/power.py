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
import json
import dbus
import dbus.service
from _dbus_glib_bindings import DBusGMainLoop
from dbus import DBusException
from gi.repository import GObject


class PowerManagerModule(object):
    def __init__(self, module):
        self._name = module['name']
        self._label = module['label']
        self._status = None

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class UPowerClient(dbus.Interface):
    def __init__(self, dispatcher=None):
        self._dbus = dbus.SystemBus(mainloop=DBusGMainLoop())
        self._proxy = self._dbus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
        dbus.Interface.__init__(self, self._proxy, 'org.freedesktop.UPower')
        self.__properties = dbus.Interface(self._proxy, 'org.freedesktop.DBus.Properties')

    @property
    def is_battery(self):
        if self.__properties is not None:
            return bool(self.__properties.Get('org.freedesktop.UPower', 'OnBattery'))
        return None


class PowerManagerClient(dbus.Interface):
    """ listen a  PropertiesChanged-Event from network-manager
    DBus object  and try to switch to powersave mode
    @todo: do not switch to powersave mode direct, needs to check
    other properties like connected ac adapter and something like this,
    replace Powersave to another Powermanager-enterpoint """

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher
        self._dispatcher.add_listener('indicator.module_toggle', self.on_module_toggle)

        self._dbus = dbus.SystemBus(mainloop=DBusGMainLoop())
        self._proxy = self._dbus.get_object('org.sensey.PowerManager', '/org/sensey/PowerManager')
        dbus.Interface.__init__(self, self._proxy, 'org.sensey.PowerManager')

    @property
    def modules_available(self):
        collection = []
        for module in json.loads(self.available(True)):
            collection.append(PowerManagerModule(module))
        return collection


    @property
    def modules_enabled(self):
        collection = []
        for module in json.loads(self.enabled(True)):
            collection.append(PowerManagerModule(module))
        return collection

    def on_module_toggle(self, event, dispatcher):
        self.toggle(event.data.name)


class PowerManagerServer(dbus.service.Object):
    def __init__(self, dispatcher, powermanager):
        DBusGMainLoop(set_as_default=True)

        self._dispatcher = dispatcher
        self._powermanager = powermanager

        try:

            dbus_service = dbus.service.BusName("org.sensey.PowerManager", dbus.SystemBus())
            dbus.service.Object.__init__(self, dbus_service, "/org/sensey/PowerManager")

        except DBusException as exception:
            print(exception.get_dbus_message())
            sys.exit(0)

        loop = GObject.MainLoop()
        loop.run()

    @dbus.service.method('org.sensey.PowerManager')
    def optimize(self, options=None):
        event = self._dispatcher.new_event()
        self._dispatcher.dispatch('power_manager.optimize', event)

    @dbus.service.method('org.sensey.PowerManager')
    def powersave(self, options):
        event = self._dispatcher.new_event()
        self._dispatcher.dispatch('power_manager.powersafe', event)

    @dbus.service.method('org.sensey.PowerManager')
    def perfomance(self, options):
        event = self._dispatcher.new_event()
        self._dispatcher.dispatch('power_manager.perfomance', event)

    @dbus.service.method('org.sensey.PowerManager')
    def available(self, options=None):
        response = []
        for switcher in self._powermanager.switchers:
            response.append({
                'name': switcher.name,
                'label': str(switcher)
            })
        return json.dumps(response)

    @dbus.service.method('org.sensey.PowerManager')
    def enabled(self, options=None):
        response = []
        for switcher in self._powermanager.managed:
            response.append({
                'name': switcher.name,
                'label': str(switcher)
            })
        return json.dumps(response)

    @dbus.service.method('org.sensey.PowerManager')
    def toggle(self, options=None):
        for switcher in self._powermanager.switchers:
            if switcher.name == options.lower():
                event = self._dispatcher.new_event(switcher)
                self._dispatcher.dispatch('network_manager.module_toggle', event)
                return True
        return False