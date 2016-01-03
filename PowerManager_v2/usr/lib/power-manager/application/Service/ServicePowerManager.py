import inspect
from vendor.Command.Command import Command
from vendor.Switcher import *
import vendor.Switcher as Switchers
from vendor.EventDispatcher import Event

class ServicePowerManager():
    """
    Initialize a main power manager object
    set up all power switchers
    """
    def __init__(self, container):
        self.container = container
        self._switchers = []
        for (name, module) in inspect.getmembers(Switchers, inspect.ismodule):
            identifier = getattr(module, name)
            self._switchers.append(identifier())
        pass


    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_powersafe', self.on_powersafe)
        service_event_dispatcher.addListener('app.on_perfomance', self.on_perfomance)
        pass


    def on_started(self, event, dispatcher):
        pass


    """
    try to switch a computer to powersave mode
    use all switchers to get a string command
    than run each command in custom thread
    """
    def on_powersafe(self, event, dispatcher):
        for switcher in self._switchers:
            for command in switcher.powersave():
                self._run(command)
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_status_changed', Event())
        pass


    """
    try to switch a computer to perfomance mode
    use all switchers to get a string command
    than run each command in custom thread
    """
    def on_perfomance(self, event, dispatcher):
        for switcher in self._switchers:
            for command in switcher.perfomance():
                self._run(command)
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_status_changed', Event())
        pass


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
    try to run a command in a custom thread
    """
    def _run(self, command):
        (Command(command)).run()