#!/usr/bin/python3

import sys
import getopt
from Powermanager import Powermanager as pm


def main(argv):
    manager = pm.Powermanager()
    manager.process((argv[0] == "true"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
