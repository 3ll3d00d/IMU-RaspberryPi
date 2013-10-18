'''

import os, fcntl, termios, sys

serialPath = '/dev/tty.usbserial-A501JT18'

ser= os.open(serialPath, 0)
[iflag, oflag, cflag, lflag, ispeed, ospeed, cc] = range(7)
settings = termios.tcgetattr(ser)
settings[ospeed] = termios.B115200
settings[ispeed] = termios.B0
print 2

'''
import csv
import serial
import time

filename = "Log." + str(time.mktime(time.localtime())) + ".csv"


with open(filename, 'wb') as csvfile:
	IMUwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

s = serial.Serial(port='/dev/tty.usbserial-A501JT18', baudrate=115200)
i = 0

while 1:
#s.write('text')
	print "A: ", i
	i += 1
	readLine =  s.readline()
	IMUwriter.writerow(readLine.split('\t'))
	print readLine.split('\t')