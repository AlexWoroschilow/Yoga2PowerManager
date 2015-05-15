#!/bin/sh
/usr/bin/dbus-send --system --print-reply \
    --dest="org.sensey.PowerManager"\
    /org/sensey/PowerManager\
    org.sensey.PowerManager.Perfomance