#!/usr/bin/python3

import sys
import getopt
from Powermanager import Powermanager as pm


def main(argv):
    if len(argv) == 1:
        powersave = argv.pop()
        if powersave in ["true", "false"]:
            manager = pm.Powermanager()
            manager.process((powersave == "true"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
