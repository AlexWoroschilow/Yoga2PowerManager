from Powermanager.Switcher.Cpu import Cpu
from Powermanager.Switcher.Hda import Hda
from Powermanager.Switcher.Sata import Sata
from Powermanager.Switcher.Usb import Usb
from Powermanager.Switcher.Pci import Pci
from Powermanager.Switcher.Watchdog import Watchdog
from Powermanager.Switcher.Wlan import Wlan
from Powermanager.Switcher.Writeback import Writeback


class Powermanager():
    def __init__(self):

        self._switchers = [];
        self._switchers.append(Cpu())
        self._switchers.append(Wlan())
        self._switchers.append(Pci())
        self._switchers.append(Usb())
        self._switchers.append(Hda())
        self._switchers.append(Sata())
        self._switchers.append(Watchdog())
        self._switchers.append(Writeback())

    def process(self, powersave):
        if powersave:
            return self.__powersave()
        return self.__perfomance()

    def __powersave(self):
        for switcher in self._switchers:
            switcher.powersave()


    def __perfomance(self):
        for switcher in self._switchers:
            switcher.perfomance()
