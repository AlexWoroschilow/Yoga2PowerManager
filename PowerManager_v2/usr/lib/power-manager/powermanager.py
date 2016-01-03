#!/usr/bin/python3

import sys
import logging

from optparse import OptionParser
from application.PowerManager import PowerManager


"""
Parse arguments an configure context
to run power manager
"""
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
