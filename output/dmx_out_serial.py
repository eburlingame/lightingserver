__author__ = 'Eric Burlingame'

import subprocess
import os
from sys import platform as _platform

import threading
import time
from DmxPy import *


OFFSET = 0.00001
class DmxOutput(object):

    def __init__(self, controller):
        self.controller = controller

    def start(self):

        self.dmxout = self.search_and_open()
        if self.dmxout == False:
            return "Could not open DMX output on serial port"

        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()                                  # Start the execution
        return "Starting interface output thread"


    def stop(self):
        self.running = False
        self.thread = None
        return "Stopping interface output thread"

    def search_and_open(self):
        dmx = DmxPy('/dev/tty.usbserial-00002014')
        return dmx
        for i in range(0, 2):
            try:
                dmx = DmxPy('/dev/ttyUSB%s' % str(i))
                return dmx
            except:
                pass
        return False


    def run(self):
        """ Method that runs forever """
        elapsed = 0.01
        while self.running:
            start = time.time()
            self.controller.update(elapsed + OFFSET)

            i = 0
            for val in self.controller.patch.dmx:
                i += 1
                val = int(val)
                self.dmxout.dmxData[i] = chr(val)
            self.dmxout.render()

            end = time.time()
            elapsed = end - start
