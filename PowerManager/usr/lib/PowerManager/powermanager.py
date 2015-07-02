#!/usr/bin/python3

import sys
import logging

from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

from Daemonocle import Daemon
from DBusService.PowerManagerService import PowerManagerService


def main(loglevel=None):
    DBusGMainLoop(set_as_default=True)

    (PowerManagerService(
        'org.sensey.PowerManager',
        '/var/log/powermanager.log',
        loglevel
    )).Optimize(None)

    (GObject.MainLoop()).run()


'''
Commands:
    # start
    # stop
    # restart

Modes:
    # CRITICAL 	50
    # ERROR 	40
    # WARNING 	30
    # INFO 	    20
    # DEBUG 	10
    # NOTSET 	0
'''
if __name__ == "__main__":
    modes = (
        logging.ERROR,
        logging.CRITICAL,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET
    )

    commands = (
        'start',
        'restart',
        'stop'
    )

    mode = logging.ERROR if len(sys.argv) <= 2 else sys.argv[2] if sys.argv[2] in modes else logging.ERROR
    command = 'start' if len(sys.argv) == 1 else sys.argv[1] if sys.argv[1] in commands else 'start'

    (Daemon(
        worker=(lambda m=mode: main(int(m))),
        pidfile='/var/run/org.sensey.Powermanager.pid',
    )).do_action(command)

