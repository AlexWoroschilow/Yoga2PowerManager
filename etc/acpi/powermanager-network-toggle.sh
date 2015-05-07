#!/bin/sh

SCRIPT="/etc/powermanager/togglenetwork.py"

if [ -f $SCRIPT -a -x $SCRIPT ]
then
    exec `$SCRIPT` >> /dev/null
fi
