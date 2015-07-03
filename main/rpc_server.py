__author__ = 'eric'

import zerorpc
import threading

class CommandRPC(object):

    def __init__(self, main):
        self.main = main

    def run_command(self, message):
        return self.main.run_server_command(message)


class RPCServer:

    def __init__(self, main):
        self.main = main

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()

    def run(self):
        s = zerorpc.Server(CommandRPC(self.main))
        s.bind("tcp://0.0.0.0:1111")
        s.run()