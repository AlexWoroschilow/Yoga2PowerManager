__author__ = 'sensey'

from Powermanager.Command.Command import Command
from Powermanager.Switcher.Cpu import Cpu
from Powermanager.Switcher.Hda import Hda
from Powermanager.Switcher.Sata import Sata
from Powermanager.Switcher.Usb import Usb
from Powermanager.Switcher.Pci import Pci
from Powermanager.Switcher.Watchdog import Watchdog
from Powermanager.Switcher.Wlan import Wlan
from Powermanager.Switcher.Writeback import Writeback
from Powermanager.Switcher.Bluetooth import Bluetooth

class Powermanager():
    def __init__(self):

        self.__switchers = [
            Cpu(),
            Wlan(),
            Pci(),
            Usb(),
            Hda(),
            Sata(),
            Watchdog(),
            Writeback(),
            Bluetooth()
        ]

    def powersave(self):
        for switcher in self.__switchers:
            for command in switcher.powersave():
                self.__run(command)

    def perfomance(self):
        for switcher in self.__switchers:
            for command in switcher.perfomance():
                self.__run(command)

    def __run(self, command):
        (Command(command)).run()