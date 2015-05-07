#!/usr/bin/python3
# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2010 Red Hat, Inc.
#

import dbus, sys


def main(argv):
    bus = dbus.SystemBus()

    # Get a proxy for the base NetworkManager object
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
    dev_iface = dbus.Interface(manager, "org.freedesktop.NetworkManager")

    dev_iface_states = {
        "NM_STATE_UNKNOWN0": 0,  # Networking state is unknown.
        "NM_STATE_ASLEEP": 10,  # Networking is inactive and all devices are disabled.
        "NM_STATE_DISCONNECTED": 20,  # There is no active network connection
        "NM_STATE_DISCONNECTING": 30,  # Network connections are being cleaned up
        "NM_STATE_CONNECTING": 40,  # A network device is connecting to a network
        "NM_STATE_CONNECTED_LOCAL": 50,  # A network device is connected, but there is only link-local connectivity
        "NM_STATE_CONNECTED_SITE": 60,  # A network device is connected, but there is only site-local connectivity
        "NM_STATE_CONNECTED_GLOBAL": 70  # A network device is connected, with global network connectivity
    }

    dev_iface_states_disabled = (
        dev_iface_states["NM_STATE_ASLEEP"],
        dev_iface_states["NM_STATE_UNKNOWN0"]
    )

    if dev_iface.state() in dev_iface_states_disabled:
        return dev_iface.Enable(True)
    dev_iface.Enable(False)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
