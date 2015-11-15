import sys
import dbus
import inspect

from gi.repository.AppIndicator3 import Indicator, IndicatorCategory, IndicatorStatus
from gi.repository import Gtk as gtk

from Application.Plugins import *
import Application.Plugins as Plugins



class IndicatorPowerManager():
    def __init__(self, filename=None, level=None):

        self.__pligins = []
        for (name, module) in inspect.getmembers(Plugins, inspect.ismodule):
            if hasattr(module, name) :
                identifier = getattr(module, name)
                self.__pligins.append(identifier(self))
        self.__pligins.sort(key=None, reverse=False);

        self.__indicator = Indicator.new(
            "Indicator Power Manager",
            "/usr/share/power-manager-indicator/share/icons/1x50px.png",
            IndicatorCategory.SYSTEM_SERVICES
        )
        self.__indicator.set_status(IndicatorStatus.ACTIVE)
        self.__indicator.set_label("\u2715", "Indicator Power Manager")
        self.__indicator.set_menu(self.menu)


    """
    Get current indicator object, needs to do 
    some manipulations in plugins and so on
    """
    @property
    def indicator(self):
        return self.__indicator


    """
    Get list of all loaded plugins
    """    
    @property
    def plugins(self):
        return self.__pligins


    """
    Render menu using plugins
    """    
    @property
    def menu(self):
        menu = gtk.Menu()
        for plugin in self.plugins :
            plugin.menu(menu)
        return menu


    """
    Interface method to set application label
    """    
    def label(self, label, description):
        self.indicator.set_label(label, description)


    """
    Interface method to refresh application state
    """    
    def refresh(self):
        self.indicator.set_menu(self.menu)
        pass


    """
    Main method to run current allication
    """    
    def main(self):
        gtk.main()


    """
    Main method to do application shutdown
    """    
    def shutdown(self, item=None):
        sys.exit(0)

