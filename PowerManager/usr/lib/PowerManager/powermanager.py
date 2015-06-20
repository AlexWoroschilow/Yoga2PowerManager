#!/usr/bin/python3

import sys
from gi.repository import Gtk
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop
from Powermanager.Service.SenseyPowerManagerService import SenseyPowerManagerService
from Daemonocle import Daemon
from Powermanager.Powermanager import Powermanager


def main():
    DBusGMainLoop(set_as_default=True)

    service = SenseyPowerManagerService(Powermanager())
    service.Optimize(None)

    loop = GObject.MainLoop()
    loop.run()

    Gtk.main()


if __name__ == "__main__":
    daemon = Daemon(
        worker=main,
        pidfile='/var/run/org.sensey.Powermanager.pid',
    )
    daemon.do_action(sys.argv[1])

