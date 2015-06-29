__author__ = 'Eric Burlingame'

import subprocess
import os
from sys import platform as _platform

import threading
import time
from dmx_py import *


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
        return "Starting interface output thread on " + self.dmxout.serialPort


    def stop(self):
        self.running = False
        self.dmxout.close()
        return "Stopping interface output thread"

    def search_and_open(self):
        p = subprocess.Popen(['ls /dev/tty* | grep -i usb'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        lines = out.split("\n")
        # print lines
        for line in lines:
            try:
                dmx = DmxPy(line)
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

            # Sometimes sending fewer packets makes fades smoother, go figure
            # time.sleep(0.03)

            end = time.time()
            elapsed = end - start
