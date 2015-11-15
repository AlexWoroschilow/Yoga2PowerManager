import sys
from gi.repository import Gtk as gtk

class Settings():
    def __init__(self, app):
        self.__app = app


    """
    Get position of menu items from this plugin
    in global indicator menu
    """
    @property
    def order(self):
        return 99
    

    """
    Build a plugin-specified menu 
    and append to common indicator menu object
    """
    def menu(self, menu):
        menu.append(self.__settings_menu("Settings"))


    """
    Build a simple menu item 
    specified for current plugin
    """
    def __settings_menu(self, label):
        element = gtk.MenuItem(label)
        element.connect("activate", self.__settings)
        element.show()
        return element;


    """
    Action for each plugin menu item
    """
    def __settings(self, item=None):
        pass


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
