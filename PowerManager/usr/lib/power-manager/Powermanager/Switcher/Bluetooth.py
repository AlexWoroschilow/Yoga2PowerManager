class Bluetooth():
    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = ["hci0"]

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            self._commands.append("/usr/sbin/hciconfig %s down &> /dev/null &" % device)
        return self._commands

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            self._commands.append("/usr/sbin/hciconfig %s up &> /dev/null &" % device)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "Bluetooth powersave mode"