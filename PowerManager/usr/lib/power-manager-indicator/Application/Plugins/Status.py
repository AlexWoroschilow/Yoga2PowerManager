import sys
import dbus
from _dbus_glib_bindings import DBusGMainLoop

from gi.repository import Gtk as gtk
from gi.repository.AppIndicator3 import Indicator, IndicatorCategory, IndicatorStatus
from Application.Plugins.StatusPlugin.DBusService.Client.PowerManager import PowerManager


class Status():
    def __init__(self, app):
        self.__app = app
        self.__manager = self.__init_manager(app)


    """
    Initialize power manager service
    """
    def __init_manager(self, app):
        return PowerManager(dbus.SystemBus(mainloop=DBusGMainLoop()), app)


    """
    Get position of menu items from this plugin
    in global indicator menu
    """
    @property
    def order(self):
        return 0


    """
    Get plugin status info, this may be a json or some
    plugin-specified objects 
    """
    @property
    def status(self):
        return self.__manager.statuses


    """
    Build a plugin-specified menu 
    and append to common indicator menu object
    """
    def menu(self, menu):
        icon = "\u2715"
        for status in self.status:
            icon = u"\u2713" if self.status[status] else "\u2715"
            menu.append(self.__switch_menu("%s %s" % (icon, status)))
        menu.append(self.__refresh_menu("Refresh status", self.__refresh))
        self.__app.label(icon, "Indicator Power Manager")


    """
    Build a simple menu item 
    specified for current plugin
    """
    def __switch_menu(self, label):
        element = gtk.MenuItem(label)
        element.connect("activate", self.__switch)
        element.show()
        return element;


    """
    Action for each plugin menu item
    """
    def __switch(self, item=None):
        pass


    """
    Build a simple menu item 
    specified for current plugin
    """
    def __refresh_menu(self, label, action):
        element = gtk.MenuItem(label)
        element.connect("activate", action)
        element.show()
        return element;


    """
    Action for each plugin menu item
    """
    def __refresh(self, item=None):
        self.__manager = self.__init_manager(self.__app)
        self.__app.refresh()


    def __lt__(self, other):
        return self.order < other.order
    
    def __gt__(self, other):
        return self.order > other.order

    def __eq__(self, other):
        return self.order == other.order

    def __le__(self, other):
        return self.order <= other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __ne__(self, other):
        return self.order != other.order
