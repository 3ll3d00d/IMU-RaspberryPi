# TO SAMPLE FOREVER: python main.py
# TO TAKE A SET NUMBER OF SAMPLES: python main.py 50

import csv,serial,os,re,sys
from datetime import datetime

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
home = os.path.expanduser("~")
filename = os.path.join(home,"logs",timestamp + ".csv")

with open(filename, 'wb') as csvfile:
    IMUwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    IMUwriter.writerow(labels)

    # read from the device
    s = serial.Serial(port='/dev/ttyUSB0', baudrate=38400)
    i = 0

    while i!=numsamples:
        print "A: ", i
        i += 1
        readLine =  s.readline()
        parsed = parseData(readLine)
        IMUwriter.writerow(parsed)
        print parsed