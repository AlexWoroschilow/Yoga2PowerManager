#!/usr/bin/python3
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import gi
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from optparse import OptionParser
sys.path.append('/usr/lib/power-manager/vendor')
import ioc

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-g", "--debug", action="store_true", default=False, dest="debug", help="enable debug mode")
    parser.add_option("-d", "--devices", action="store_true", default=False, dest="devices", help="show devices")
    parser.add_option("-m", "--modules", action="store_true", default=False, dest="modules", help="show switchers")
    parser.add_option("-s", "--states", action="store_true", default=False, dest="states", help="show current states")

    (options, args) = parser.parse_args()

    container = ioc.build(['/usr/lib/power-manager/vendor/services.yml'])
    config = container.get('config')
    power_manager = container.get('power_manager')

    if options.devices:
        for switcher in power_manager.switchers:
            for device in switcher.devices:
                ignored = config.ignored(switcher.name)
                print("%15s, %55s \t%s" % (switcher, str(device), ('ignored' if ignored else 'managed')))

    if options.modules:
        for switcher in power_manager.switchers:
            ignored = config.ignored(switcher.name)
            print("%15s \t%s" % (switcher, ('ignored' if ignored else 'managed')))

    if options.states:
        for switcher in power_manager.switchers:
            powersafe = switcher.is_powersave
            print("%15s \t%5s" % (switcher, 'powersafe' if powersafe else 'perfomance'))

    Gtk.main()

