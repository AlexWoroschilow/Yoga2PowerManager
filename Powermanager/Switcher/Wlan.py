import os
from Powermanager.Command.Command import Command
from Powermanager.Switcher.Switcher import Switcher

__author__ = 'sensey'


class Wlan(Switcher):
    def __init__(self):
        self._devices = ["wlan0"]

    def powersave(self):
        for device in self._devices:
            (Command("/sbin/iw dev %s set power_save on" % device)).run()


    def perfomance(self):
        for device in self._devices:
            (Command("/sbin/iw dev %s set power_save off" % device)).run()

