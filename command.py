__author__ = 'eric'
import sys
from websocket import create_connection

# Calls a single set of commands once; this script can be called by other programs to runn commands easily

command = ""

i = 0
for arg in sys.argv:
    if i != 0:
        command += arg
    i += 1

ws = create_connection("ws://localhost:8080/ws")

print "Calling '%s'" % command
ws.send(command)

result =  ws.recv()
print "Response: '%s'" % result

ws.close()

