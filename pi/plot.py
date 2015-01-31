# TO SAMPLE FOREVER: python main.py
# TO TAKE A SET NUMBER OF SAMPLES: python main.py 50

#original imports
import csv,serial,os,re,sys,time
from datetime import datetime
#new imports
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

# Analog data: 0: pitch / 1: roll / 2: yaw / 3: accelX / 4: accelY / 5: accelZ
labels = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"]
channel = ["AN0","AN1","AN2","AN3","AN4","AN5","LAT","LON","ALT","FIX"]

def parseData(data):
    sample = []
    for i in range(10):
        pattern = re.compile(r".*"+channel[i]+r":([\-\d\.]+).*")
        matched = pattern.match(data)
        if matched:
            if channel[i]=="LAT" or channel[i]=="LON":
                num = float(matched.group(1))/(10**7)
            elif channel[i]=="ALT":
                num = float(matched.group(1))/(10**1)
            else:
                num = float(matched.group(1))
            sample.append(num)
        else:
            sample.append(0)

    return sample

numsamples = -1 # sample forever by default
if len(sys.argv) > 1:
    numsamples = int(sys.argv[1])

    if len(sys.argv) > 2:
        directory = sys.argv[2]
    else:
        directory = "logs"

# open a logging file
timestamp = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
path = "/Users/Jordan/Documents/REVO/imulogs" # change this to your username
if not os.path.exists(path):
    os.makedirs(path)
filename = os.path.join(path,timestamp + ".csv")

#with open(filename, 'wb') as csvfile:
#    IMUwriter = csv.writer(csvfile, delimiter=',',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    IMUwriter.writerow(labels)

    # read from the device
s = serial.Serial(port='/dev/tty.usbserial-A7027EKU', baudrate=38400)
i = 0
fig=plt.figure()

pitch = np.linspace(0, numsamples, numsamples)
#     while i!=numsamples:
#         print "A: ", i
#         i += 1
#         readLine =  s.readline()
#         parsed = parseData(readLine)
#         IMUwriter.writerow(parsed)
#         print parsed
# ###########################end of original code#################################
# #      
# #
# #
# ############################start of new code using matplotlib###################
    
ax = plt.axes(xlim=(0,numsamples), ylim=(-5000,1500))
#plt.legend(handles = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"])
#         pitch.append(parsed[1])
#         # roll = []
#         # yaw = []
#         # accelX = []
#         # accelY =[]
#         # accelZ =[]
line, = ax.plot([], [], lw=10)
#         # line2, = ax.plot([], [], lw=10)
#         # line3, = ax.plot([], [], lw=10)
#         # line4, = ax.plot([], [], lw=10)
#         # line5, = ax.plot([], [], lw=10)
#         # line6, = ax.plot([], [], lw=10)

def init():
    line.set_data([], [])  #pitch
#             # line2.set_data([], []) #roll
#             # line3.set_data([], []) #yaw
#             # line4.set_data([], []) #accelX
#             # line5.set_data([], []) #accelY
#             # line6.set_data([], []) #accelZ
#             return line, #line2, line3, line4, line5, line6,
#         # def init():
#         #     pitch.set_data([], [])
#         #     yaw.set_data([], [])


def animate(i):
    if (i < numsamples):
        parsed = parseData(s.readline())
        print(i, parsed)

        x = np.linspace(0, numsamples, numsamples)
        pitch[i] = parsed[1]
    else:
        raw_input()
    line.set_data(x, pitch)
        
    return line, 
#             # line2.set_data(x, parsed[2])
#             # line3.set_data(x, parsed[3])
#             # line4.set_data(x, parsed[4])
#             # line5.set_data(x, parsed[5])
#             # line6.set_data(x, parsed[6])
#             return line, #line2, line3, line4, line5, line6,
anim = animation.FuncAnimation(fig, animate, init_func=init, \
                               frames=100, interval=20, blit=False)
        

# plt.show()
#time.sleep(0.1)
# plt.pause(0.1)

# s.close()
# raw_input()