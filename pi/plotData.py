# plot the analog data
# TO RUN: python plotData.py 2014-01-19_14:56:32.csv

import csv,sys
import matplotlib.pyplot as plt

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

    for i in range(6):
        plt.plot(rawData[labels[i]],color=colors[i],label=labels[i])

    plt.legend()
    plt.show()
    
else:
    print "Please specify a .csv"