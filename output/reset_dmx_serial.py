import serial, sys, time

DMXOPEN = chr(126)
DMXCLOSE = chr(231)
DMXINTENSITY=chr(6)+chr(1)+chr(2)				
DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)
DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)


