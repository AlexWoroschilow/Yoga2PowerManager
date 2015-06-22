#!/usr/bin/python3

import sys, logging
from logging.handlers import RotatingFileHandler
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop
from Powermanager.Service.SenseyPowerManagerService import SenseyPowerManagerService
from Daemonocle import Daemon
from Powermanager.Powermanager import Powermanager


def main(level=None):
    DBusGMainLoop(set_as_default=True)

    logger = logging.getLogger('org.sensey.PowerManager')
    logging.basicConfig(level=level, filename='/var/log/powermanager.log')

    service = SenseyPowerManagerService(Powermanager(logger), logger)
    service.Optimize(None)

    (GObject.MainLoop()).run()


if __name__ == "__main__":
    # start
    # stop
    # restart
    command = 'start'
    if sys.argv.__len__() > 1:
        command = sys.argv[1]
    # CRITICAL 	50
    # ERROR 	40
    # WARNING 	30
    # INFO 	    20
    # DEBUG 	10
    # NOTSET 	0
    mode = logging.ERROR
    if sys.argv.__len__() >= 3:
        mode = sys.argv[2]

    (Daemon(
        worker=(lambda m=mode: main(int(m))),
        pidfile='/var/run/org.sensey.Powermanager.pid',
    )).do_action(command)

