#!/usr/bin/env python
"""Controlling spotify with gnome media keys via dbus-python.
"""

import sys
import traceback
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

## 
# Define Functions
##
def on_mediakey(comes_from, what):
    """ gets called when multimedia keys are pressed down.
    """
    if what == 'Play':
        what = 'PlayPause'
    try:
        eval('spotify_bus.' + what + "(dbus_interface='org.mpris.MediaPlayer2.Player')")
    except dbus.DBusException:
        traceback.print_exc()

##
#Start the show
##
# Set up the glib main loop.
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

# Grab the spotify control daemon
try:
    gnome_media_bus = bus.get_object('org.gnome.SettingsDaemon', 
                        '/org/gnome/SettingsDaemon/MediaKeys')
except dbus.DBusException:
    traceback.print_exc()
    print "spotify-dbus failed grabbing gnome_media_bus"
    sys.exit(1)

# Grab the gnome MediaKey daemon
try:
    spotify_bus = bus.get_object('org.mpris.MediaPlayer2.spotify',
                        '/org/mpris/MediaPlayer2')
except dbus.DBusException:
    traceback.print_exc()
    print "spotify-dbus failed grabbing spotify_bus"
    sys.exit(1)

# Tell SettingsDaemon.MediaKeys that we'd like to know when a key is pressed...
gnome_interface='org.gnome.SettingsDaemon.MediaKeys'
gnome_media_bus.GrabMediaPlayerKeys("spotify-dbus", 0, 
                               dbus_interface=gnome_interface)

# ...then use connect_to_signal to lash our callback function on_mediakey to any resulting signal.
gnome_media_bus.connect_to_signal('MediaPlayerKeyPressed', on_mediakey)

# then let's go and start the main loop to keep listening for events.
mainloop = gobject.MainLoop()
mainloop.run()

