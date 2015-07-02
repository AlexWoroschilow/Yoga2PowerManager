import os
from Powermanager.Switcher.Switcher import Switcher


class Bluetooth(Switcher):
    def __init__(self):
        self._devices = ["hci0"]

    def powersave(self):
        commands = []
        for device in self._devices:
            commands.append("/usr/sbin/hciconfig %s down &> /dev/null &" % device)
        return commands

    def perfomance(self):
        commands = []
        for device in self._devices:
            commands.append("/usr/sbin/hciconfig %s up &> /dev/null &" % device)
        return commands