"""

@authors: brennamanning, jovanduy, redfern314

Reads accelerometer data from csv file
Creates animated plot of recorded data on a circular graph

TO RUN: python circleGraph.py (CSV FILE NAME)
ex:
TO RUN: python circleGraph.py 2014-01-19_14:56:32.csv

"""

import csv,sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ACCEL_CONVERSION = 4096
colors = ["r","b","g","c","m","k"]
labels = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"]


def read_csv_and_plot_figure():

    for i in range(6):
        rawData[labels[i]] = []

    with open(filename, 'rb') as csvfile:
        IMUreader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fig= plt.figure(1)
        ax=fig.add_subplot(1,1,1)
        circle1 = plt.Circle((0,0), radius = 2, color = 'r', fill = False)
        plt.plot([-.0001,.0001],[-2,2],'k-')
        plt.plot([-2,2],[-.0001,.0001],'k-')
        ax.set_xlim((-2,2))
        ax.set_ylim((-2,2))
        ax.add_patch(circle1)

        # read all the data
        for row in IMUreader:
            if row[0] != "pitch": # first row is headers
                rawData["pitch"].append(float(row[0]))
                rawData["roll"].append(float(row[1]))
                rawData["yaw"].append(float(row[2]))
                rawData["accelX"].append(float(row[3])/ACCEL_CONVERSION)
                rawData["accelY"].append(float(row[4])/ACCEL_CONVERSION)
                rawData["accelZ"].append(float(row[5]))
                ax.add_patch(circle1)
                fig.clf()
                circle1 = plt.Circle((0,0), radius = 2, color = 'r', fill = False)
                plt.plot([-.0001,.0001],[-2,2],'k-')
                plt.plot([-2,2],[-.0001,.0001],'k-')
                ax.set_xlim((-2,2))
                ax.set_ylim((-2,2))
                fig.gca().add_artist(circle1)
                plt.plot(rawData["accelX"][-1],rawData["accelY"][-1], marker='o', color='blue',linestyle='None')
                plt.pause(0.01)


    plt.legend()
    plt.show()

if len(sys.argv) > 1:
    filename = sys.argv[1]
    rawData = {}  
    read_csv_and_plot_figure()  
else:
    print "Please specify a .csv"