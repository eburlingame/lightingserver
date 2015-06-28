__author__ = 'eric'

# This is designed to use the usbreset program (https://gist.github.com/x2q/5124616)
# to reset the port of a Enttec DMX USB Pro, which is not recognized by OLA until
# it has been reset after the system boots up

import subprocess
import os


