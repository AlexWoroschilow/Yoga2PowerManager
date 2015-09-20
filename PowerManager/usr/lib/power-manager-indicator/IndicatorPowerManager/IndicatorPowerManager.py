import sys
import dbus
from _dbus_glib_bindings import DBusGMainLoop
from gi.repository.AppIndicator3 import Indicator, IndicatorCategory, IndicatorStatus
from DBusService.Client.PowerManager import PowerManager
from gi.repository import Gtk as gtk


class IndicatorPowerManager():
    def __init__(self, filename=None, level=None):

        self.__power_manager = PowerManager(
            dbus.SystemBus(mainloop=DBusGMainLoop()),
            self
        )


        self.__indicator = Indicator.new(
            "Indicator Power Manager",
            "/usr/share/power-manager-indicator/share/icons/1x50px.png",
            IndicatorCategory.SYSTEM_SERVICES
        )
        self.__indicator.set_status(IndicatorStatus.ACTIVE)
        self.__indicator.set_menu(self.menu)


    def status_changed(self):
        self.__indicator.set_menu(self.menu)
        pass

    @property
    def menu(self):
        menu = gtk.Menu()
        states = self.__power_manager.statuses
        for item in states:
            panel_icon = "\u2715"
            if states[item]:
                panel_icon = u"\u2713"
            menu.append(self.__menu_item("%s %s" % ( panel_icon, item), lambda x, y=item: self.__switch_state(x, y)))
        self.__indicator.set_label(panel_icon, "Indicator Power Manager")
        return menu

    def __switch_state(self, item=None, module=None):
        # print(item.get_label(), module)
        pass


    def __menu_item(self, name, action):
        element = gtk.MenuItem(name)
        element.connect("activate", action)
        element.show()
        return element


    def main(self):
        gtk.main()

    def __shutdown(self, menu_item=None):
        sys.exit(0)

