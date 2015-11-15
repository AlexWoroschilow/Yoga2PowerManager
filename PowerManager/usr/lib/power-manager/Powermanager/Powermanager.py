import inspect
from Powermanager.Switcher import *
import Powermanager.Switcher as Switchers
from Powermanager.Command.Command import Command


class Powermanager():
    """
    Initialize a main power manager object
    set up all power switchers
    """
    def __init__(self, logger):
        self._switchers = []
        for (name, module) in inspect.getmembers(Switchers, inspect.ismodule):
            identifier = getattr(module, name)
            self._switchers.append(identifier())
        self._logger = logger


    """
    Get list of switcher objects,
    this objects do a switch between 
    powersave and perfomance mode 
    for different devices
    """
    @property
    def switchers(self):
        return self._switchers


    """
    try to switch a computer to powersave mode
    use all switchers to get a string command
    than run each command in custom thread
    """
    def powersave(self):
        self._log('powersave')
        for switcher in self._switchers:
            for command in switcher.powersave():
                self._run(command)


    """
    try to switch a computer to perfomance mode
    use all switchers to get a string command
    than run each command in custom thread
    """
    def perfomance(self):
        self._log('perfomance')
        for switcher in self._switchers:
            for command in switcher.perfomance():
                self._run(command)


    """
    write logs using given logger class
    """
    def _log(self, text):
        if self._logger is not None:
            self._logger.debug(text)


    """
    try to run a command in a custom thread
    """
    def _run(self, command):
        self._logger.info(command)
        (Command(command)).run()