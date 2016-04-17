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
from logging import *
from logging.handlers import RotatingFileHandler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from optparse import OptionParser
# os.chdir('/usr/lib/power-manager')
sys.path.append('vendor')
import ioc

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-g", "--debug", action="store_true", default=False, dest="debug", help="enable debug mode")
    parser.add_option("-d", "--devices", action="store_true", default=False, dest="devices", help="show devices")
    parser.add_option("-m", "--modules", action="store_true", default=False, dest="modules", help="show switchers")
    parser.add_option("-s", "--states", action="store_true", default=False, dest="states", help="show current states")
    parser.add_option("-l", "--loglevel", default=INFO, dest="loglevel", help="logging level")
    parser.add_option("-f", "--format", default="%(asctime)s\t- %(levelname)s\t- %(name)s - %(message)s", dest="format", help="format for log string")
    parser.add_option("-o", "--logfile", default='/var/log/power-manager.log', dest="logfile", help="Logfile destination")

    (options, args) = parser.parse_args()
    basicConfig(level=options.loglevel, format=options.format, handlers=[
        RotatingFileHandler(filename=options.logfile, maxBytes=(1024 * 100), backupCount=3)
    ])

    container = ioc.build(['vendor/services.yml'])
    config = container.get('config')
    manager = container.get('power_manager')

    if options.devices:
        logger = getLogger()
        logger.addHandler(StreamHandler())
        for switcher in manager.switchers:
            for device in switcher.devices:
                ignored = config.ignored(switcher.name)
                logger.info("%15s, %55s \t%s" % (switcher, str(device), ('ignored' if ignored else 'managed')))

    if options.modules:
        logger = getLogger()
        logger.addHandler(StreamHandler())
        for switcher in manager.switchers:
            ignored = config.ignored(switcher.name)
            logger.info("%15s \t%s" % (switcher, ('ignored' if ignored else 'managed')))

    if options.states:
        logger = getLogger()
        logger.addHandler(StreamHandler())
        for switcher in manager.switchers:
            powersafe = switcher.is_powersave
            logger.info("%15s \t%5s" % (switcher, 'powersafe' if powersafe else 'perfomance'))

    if not options.devices and not options.states and not options.modules:
        container.get('server_dbus_power_manager').start()
        Gtk.main()
