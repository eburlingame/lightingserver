__author__ = 'eric'

# This is designed to use the usbreset program (https://gist.github.com/x2q/5124616)
# to reset the port of a Enttec DMX USB Pro, which is not recognized by OLA until
# it has been reset after the system boots up

import subprocess
import os
import re


ftdi_id = "0403:6001"

p = subprocess.Popen(['lsusb', '-d', ftdi_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

if err != "":
    print "Could not find DMX USB Pro, Error: %s" % err

pattern = "Bus (\d+) Device (\d+): ID:(\d+):(\d+) (.+)"
match = re.match(pattern, out)
if match:
    groups = match.groups()
    bus = groups[0]
    port = groups[1]
    addr = "/dev/bus/usb/%s/%s" % (bus, port)
    p = subprocess.Popen(['sudo', '~/./usbreset', addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
else:
    "Output did not match expected format"



