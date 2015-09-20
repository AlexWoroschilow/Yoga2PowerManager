class WebCam():
    """
    Web Camera kernel module switcher
    remove module for powersave mode
    and insert module for perfomance mode
    """

    def __init__(self):
        self._commands = []
        self._powersave = False
        self._devices = ["uvcvideo"]

    """
    remove web camera module to save energy
    """

    def powersave(self):
        self._commands.clear()
        self._powersave = True
        for device in self._devices:
            self._commands.append("/sbin/modprobe -r %s" % device)
        return self._commands

    """
    enable web camera for perfomance mode
    """

    def perfomance(self):
        self._commands.clear()
        self._powersave = False
        for device in self._devices:
            self._commands.append("/sbin/modprobe %s" % device)
        return self._commands

    @property
    def is_powersave(self):
        return self._powersave

    @property
    def devices(self):
        return self._devices

    def __str__(self):
        return "Web camera kernel module"