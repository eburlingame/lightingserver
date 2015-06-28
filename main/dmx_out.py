__author__ = 'Eric Burlingame'

import threading
import time
import array
from ola.ClientWrapper import ClientWrapper

OFFSET = 0.00001
class DmxOutput(object):

    def __init__(self, controller):
        self.controller = controller

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()                                  # Start the execution

    def stop(self):
        self.running = False
        self.thread = None


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