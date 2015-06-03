__author__ = 'Eric Burlingame'

from controller import Controller

def main():
    controller = Controller()
    print "LightingServer starting..."
    cmd = ""
    while cmd != "quit":
        cmd = raw_input(">>>")



main()