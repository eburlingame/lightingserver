__author__ = 'Eric Burlingame'

import subprocess
import os
from sys import platform as _platform

import threading
import time
import array
from ola.ClientWrapper import ClientWrapper


OFFSET = 0.00001
class DmxOutput(object):

    def __init__(self, controller):
        self.controller = controller

    def start(self):
        str = ""
        # if _platform == "linux2": # If we're on a raspberry pi
            # self.reset_usb()
            # str += "Resetting usb; "

        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()                                  # Start the execution
        return str +"Starting interface output thread"

    # Some interfaces (Enttec DMX USB Pro) need to be reset and re-recognized by OLA
    def reset_usb(self):
        # cmd = "$(lsusb -d 12d1:1506 | awk -F '[ :]'  '{ print \"/dev/bus/usb/\"$2\"/\"$4 }' | xargs -I {} echo \"~/./usbreset {}\")"
        for i in range(0, 10): # Cycle all ports 1-20
            bus = "001"
            port = ""
            if i < 10:
                port = "00" + str(i)
            else:
                port = "0" + str(i)
            file = "/dev/bus/usb/%s/%s" % (bus, port)
            FNULL = open(os.devnull, 'w')
            subprocess.call(["~/./usbreset", file])

    def stop(self):
        self.running = False
        self.thread = None
        return "Stopping interface output thread"


    def run(self):
        """ Method that runs forever """
        universe = 1
        wrapper = ClientWrapper()

        def DmxSent(state):
            wrapper.Stop()

        elapsed = 0.01
        while self.running:
            start = time.time()
            self.controller.update(elapsed + OFFSET)

            toSend = []
            i = 0
            for val in self.controller.patch.dmx:
                i += 1

                toSend.append(int(val))

            data = array.array('B', toSend)
            client = wrapper.Client()
            client.SendDmx(universe, data, DmxSent)
            wrapper.Run()

            end = time.time()
            elapsed = end - start