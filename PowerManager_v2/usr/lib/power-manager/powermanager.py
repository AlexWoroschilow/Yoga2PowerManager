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
from optparse import OptionParser
from application.PowerManager import PowerManager

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-g", "--debug", action="store_true", default=False, dest="debug", help="enable debug mode")
    parser.add_option("-d", "--devices", action="store_true", default=False, dest="devices", help="show devices")
    parser.add_option("-m", "--modules", action="store_true", default=False, dest="modules", help="show switchers")
    parser.add_option("-s", "--states", action="store_true", default=False, dest="states", help="show current states")

    (options, args) = parser.parse_args()

    application = PowerManager()

    application.devices() \
        if options.devices \
        else application.modules() \
        if options.modules \
        else application.status() \
        if options.states \
        else application.start()
