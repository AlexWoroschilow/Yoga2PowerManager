#!/usr/bin/env python3

# Copyright 2015 Alex Woroschilow
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
# See the License for the specific language governing permissions and
# limitations under the License.
import gi
import sys
from optparse import OptionParser
from logging import *
from logging.handlers import RotatingFileHandler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
sys.path.append('/usr/lib/power-manager/vendor')
import ioc

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-l", "--loglevel", default=WARNING, dest="loglevel", help="logging level")
    parser.add_option("-f", "--format", default="%(asctime)s\t- %(levelname)s\t- %(name)s - %(message)s", dest="format", help="format for log string")
    parser.add_option("-o", "--logfile", default='/tmp/power-manager-indicator.log', dest="logfile", help="Logfile destination")

    (options, args) = parser.parse_args()
    basicConfig(level=options.loglevel, format=options.format, handlers=[
        RotatingFileHandler(filename=options.logfile, maxBytes=(1024 * 100), backupCount=3)
    ])

    ioc.build(['/usr/lib/power-manager/vendor/services-indicator.yml'])
    Gtk.main()