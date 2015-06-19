__author__ = 'eric'

import threading
import time
import array
from ola.ClientWrapper import ClientWrapper


class DmxOutput(object):
    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, patch, interval = 1):

        self.interval = interval
        self.patch = patch

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution


    def run(self):
        """ Method that runs forever """
        universe = 1
        wrapper = ClientWrapper()

        def DmxSent(state):
            wrapper.Stop()

        while True:
            self.patch.update_channels(self.interval)

            toSend = []
            i = 0
            for val in self.patch.dmx:
                i += 1
                if i == 1:
                    if val != 255:
                        "not 255!"

                toSend.append(int(val))

            data = array.array('B', toSend)
            client = wrapper.Client()
            client.SendDmx(universe, data, DmxSent)
            wrapper.Run()

            time.sleep(self.interval)
