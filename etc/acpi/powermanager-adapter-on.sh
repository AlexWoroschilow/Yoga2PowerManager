#!/bin/sh

SCRIPT="/etc/powermanager/powermanager.py"

if [ -f $SCRIPT -a -x $SCRIPT ]
then
    exec `$SCRIPT false` >> /dev/null
fi
