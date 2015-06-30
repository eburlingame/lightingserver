__author__ = 'eric'
__author__ = 'Eric Burlingame'

import subprocess
import os
from sys import platform as _platform

import threading
import time
from dmx_py import *


OFFSET = 0.00001
class DummyOutput(object):

    def __init__(self, controller):
        self.controller = controller

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()                                  # Start the execution
        return "Starting dummy output"


    def stop(self):
        self.running = False
        return "Stopping dummy output"

    def run(self):
        """ Method that runs forever """
        elapsed = 0.01
        while self.running:
            start = time.time()
            self.controller.update(elapsed + OFFSET)

            end = time.time()
            elapsed = end - start
