__author__ = 'eric'
import time
from main.patch import *

patch = Patch()

patch.patch_channel(1, 1, "Channel 1")
patch.patch_channel(2, 2, "Channel 2")
patch.patch_channel(3, 3, "Channel 3")
patch.patch_channel(4, 4, "Channel 4")

print "Fading up"
patch.channels[0].fadeTo(100, 0)
patch.channels[1].fadeTo(50, 3)
patch.channels[2].fadeTo(100, 3)
patch.channels[3].fadeTo(100, 0)

rate = 1
i = 0
while True:
    time.sleep(rate)
    patch.update_channels(rate)
    print patch.dmx

    i += 1

    if i == 5:
        print "Fading out"
        patch.channels[0].fadeTo(0, 0)
        patch.channels[1].fadeTo(0, 3)
        patch.channels[2].fadeTo(0, 3)
        patch.channels[3].fadeTo(0, 0)

    if i == 10:
        print "Fading to 50"
        patch.channels[0].fadeTo(50, 10)
        patch.channels[1].fadeTo(50, 10)
        patch.channels[2].fadeTo(50, 10)
        patch.channels[3].fadeTo(50, 10)