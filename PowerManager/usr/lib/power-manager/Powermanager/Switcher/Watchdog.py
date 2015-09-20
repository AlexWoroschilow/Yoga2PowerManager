import os
import os.path


class Watchdog():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = ["/proc/sys/kernel/nmi_watchdog"]

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            if os.path.isfile(device):
                self._commands.append("echo '0' > '%s';" % device)
        return self._commands

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            if os.path.isfile(device):
                self._commands.append("echo '1' > '%s';" % device)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "Watchdog optimisations"