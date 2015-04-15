# plot the analog data
# TO RUN: python plotData.py 2014-01-19_14:56:32.csv

import csv,sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

colors = ["r","b","g","c","m","k"]
labels = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"]

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

if len(sys.argv) > 1:
    filename = sys.argv[1]

    rawData = {}
    for i in range(6):
        rawData[labels[i]] = []

    with open(filename, 'rb') as csvfile:
        IMUreader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # read all the data
        for row in IMUreader:
            if row[0] != "pitch": # first row is headers
                rawData["pitch"].append(float(row[0]))
                rawData["roll"].append(float(row[1]))
                rawData["yaw"].append(float(row[2]))
                rawData["accelX"].append(float(row[3]))
                rawData["accelY"].append(float(row[4]))
                rawData["accelZ"].append(float(row[5]))
      
    
else:
    print "Please specify a .csv"   

def data_gen():
    t = data_gen.t
    print ("accel x", len(rawData["accelX"]))
    if t < len(rawData["accelX"]):
        print "HELP"
        t += 1
        yield t, rawData["accelX"][t]
data_gen.t = 0 
"""
def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt+=1
        t += 0.05
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
data_gen.t = 0
"""


fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
#ax.set_ylim(-1.1, 1.1)
#ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []
def run(data):
    # update the data
    print("data", data)
    t,y = data
    print ("t" , t)
    print ("y" , y)
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,


#def animate(i):
 #   ax1.clear()
#    ax1.plot(t, rawData["accelX"])        
test = data_gen()
print(test)
#ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval= 10, repeat = False)
ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10, repeat=False)
plt.show()


#plt.plot(t, rawData["accelX"])
#plt.show


    #for i in range(6):
        #plt.plot(rawData[labels[i]],color=colors[i],label=labels[i])

    #plt.legend()
    #plt.show()
    