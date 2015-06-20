__author__ = 'Eric Burlingame'

import threading
import time
import array
from ola.ClientWrapper import ClientWrapper

OFFSET = 0.00001
class DmxOutput(object):
    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, controller):

        self.controller = controller

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution


    def run(self):
        """ Method that runs forever """
        universe = 1
        wrapper = ClientWrapper()

        def DmxSent(state):
            wrapper.Stop()

        elapsed = 0.01
        while True:
            start = time.time()
            self.controller.update(elapsed + OFFSET)

            toSend = []
            i = 0
            for val in self.controller.patch.dmx:
                i += 1
                if i == 1:
                    if val != 255:
                        "not 255!"

                toSend.append(int(val))

            data = array.array('B', toSend)
            client = wrapper.Client()
            client.SendDmx(universe, data, DmxSent)
            wrapper.Run()

            end = time.time()
            elapsed = end - start

