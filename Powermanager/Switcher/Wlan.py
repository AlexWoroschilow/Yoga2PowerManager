import os
from Powermanager.Switcher.Switcher import Switcher

__author__ = 'sensey'


class Wlan(Switcher):
    def __init__(self):
        self._devices = []

    def powersave(self):
        os.system("/sbin/iw dev wlan0 set power_save on")

    def perfomance(self):
        os.system("/sbin/iw dev wlan0 set power_save off")
