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
    def __init__(self, logger):

        self._logger = logger

        self._switchers = [
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

    @property
    def logger(self):
        return self._logger

    def powersave(self):
        self.logger.debug('powersave')
        for switcher in self._switchers:
            for command in switcher.powersave():
                self._run(command)

    def perfomance(self):
        self.logger.debug('perfomance')
        for switcher in self._switchers:
            for command in switcher.perfomance():
                self._run(command)

    def _run(self, command):
        self.logger.info(command)
        (Command(command)).run()