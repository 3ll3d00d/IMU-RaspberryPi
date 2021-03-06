"""
    plot the analog data
    TO RUN: python xyGraphAnimated.py 2014-01-19_14:56:32.csv

    @authors: jovanduy, brennamanning, redfern314
"""

# plot the analog data
# TO RUN: python xyGraphAnimated.py 2014-01-19_14:56:32.csv

import csv,sys
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

colors = ["r","b","g","c","m","k"]
labels = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"]

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


    
    def data_gen():
        t = data_gen.t
        i = 0
        while i < len(rawData["accelX"]):
            i += 1
            t += 1
            yield t, rawData["accelX"][t], rawData["accelY"][t]
    data_gen.t = 0

    fig, ax = plt.subplots()
    linexaccel, = ax.plot([], [], lw=2)
    lineyaccel, = ax.plot([], [], lw=2)
    ax.set_ylim(-20000.0, 20000.0)
    ax.set_xlim(0, 50)
    ax.grid()
    time, xacceldata, yacceldata = [], [], []
    def run(data):
        # update the data
        t,x,y = data
        time.append(t)
        xacceldata.append(x)
        yacceldata.append(y)
        xmin, xmax = ax.get_xlim()

        if t >= xmax:
            ax.set_xlim(xmin, 2*xmax)
            ax.figure.canvas.draw()
        linexaccel.set_data(time, xacceldata)
        lineyaccel.set_data(time, yacceldata)


        return linexaccel, lineyaccel

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
        repeat=False)
    plt.show()
    

    # for i in range(6):
    #     plt.plot(rawData[labels[i]],color=colors[i],label=labels[i])

    # plt.legend()
    # plt.show()
    
else:
    print "Please specify a .csv"
