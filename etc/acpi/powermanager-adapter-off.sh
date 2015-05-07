#!/bin/sh

SCRIPT="/etc/powermanager/powermanager.py"

if [ -f $SCRIPT -a -x $SCRIPT ]
then
    exec `$SCRIPT true` >> /dev/null
fi
