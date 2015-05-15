#!/usr/bin/python3

import dbus
import dbus.service
from gi.repository import Gtk
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop
from Powermanager.Service.SenseyPowerManagerService import SenseyPowerManagerService
from Powermanager.ClientNetworkManager.ClientNetworkManager import ClientNetworkManager


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
    ClientNetworkManager(proxy, 'org.freedesktop.NetworkManager', SenseyPowerManagerService())

    loop = GObject.MainLoop()
    loop.run()

    Gtk.main()



