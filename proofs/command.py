__author__ = 'eric'
from websocket import create_connection

# Calls a single set of commands once; this script can be called by other programs to runn commands easily

commands = [
    "load scene test"
]


ws = create_connection("ws://localhost:8080/ws")

for command in commands:

    print "Calling '%s'" % command
    ws.send(command)

    result =  ws.recv()
    print "Response: '%s'" % result

ws.close()

