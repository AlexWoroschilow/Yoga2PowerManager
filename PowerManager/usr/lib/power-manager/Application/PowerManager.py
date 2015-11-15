import json
from  logging import *
from dbus import DBusException
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop
import sys
from DBusService.PowerManagerService import PowerManagerService
from Powermanager.Powermanager import Powermanager


class PowerManager():
    def __init__(self, debug=False, name='org.sensey.PowerManager', file='/var/log/powermanager.log'):
        self.__name = name
        self.__file = file
        self.__level = DEBUG if \
            debug else ERROR

        basicConfig(
            level=self.__level,
            filename=self.__file
        )

        self._logger = getLogger(self.__name)
        self._power_manager = Powermanager(self._logger)


    """
    Start DBus service and DBus listeners
    try to optimize power usage using current context
    """
    def service(self):
        DBusGMainLoop(set_as_default=True)

        try:
            (PowerManagerService(
                self.__name,
                self._power_manager,
                self._logger
            )).optimize(None)

        except DBusException as exception:
            self._logger.critical(exception.get_dbus_message())
            sys.exit(0)

        (GObject.MainLoop()).run()


    """
    Show all available and enabled modules
    for current power manager context
    """
    def modules(self):
        for switcher in self._power_manager.switchers:
            print("Module:\t%10s" % (switcher))


    """
    Show all current power states over module
    for current power manager context
    """
    def states(self):
        for switcher in self._power_manager.switchers:
            print("Module:\t%10s, \tPowersave: %5s" % (switcher, switcher.is_powersave))


    """
    Show all available devices
    for current power manager context
    """
    def devices(self):
        for switcher in self._power_manager.switchers:
            for device in switcher.devices:
                print("Module:\t%10s, Device: %40s" % (switcher, device))
