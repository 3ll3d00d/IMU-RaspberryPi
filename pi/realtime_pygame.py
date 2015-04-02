# TO SAMPLE FOREVER: python main.py
# TO TAKE A SET NUMBER OF SAMPLES: python main.py 50

import csv,serial,os,re,sys,pygame,time
from datetime import datetime
from pygame.locals import *
from math import sqrt

background_colour = (0,0,0)
(width, height) = (350, 350)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('')
screen.fill(background_colour)    
pygame.display.flip()
pygame.display. set_caption('Acceleration')
#set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
GRAY = (100, 100, 100)


def remap_interval(val, input_interval_start = -.5, input_interval_end = .5, output_interval_start = 0, output_interval_end = 350):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].
    """
    return int(((val - input_interval_start) * (output_interval_end - output_interval_start) / float(input_interval_end - input_interval_start) + output_interval_start))
   

def draw_backround():
    """Draw background"""
    pygame.deraw.line(screen, GRAY, (remap_interval(-2), remap_interval(0)), (remap_interval(2),remap_interval(0)), 1)
    pygame.draw.line(screen, GRAY, (remap_interval(0), remap_interval(-2)), (remap_interval(0), remap_interval(2)), 1)
    pygame.draw.circle(screen, RED, (175, 175), 170, 1)

def initialize_font():
    """Initializes font for text"""
    pygame.font.init()
    myfont = pygame.font.SysFont("freesansbold", 20)





def parseData(data):
    sample = []
    for i in range(11):
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
path = "home/REVO/IMU-RaspberryPi/pi/logs" # change this to your username
if not os.path.exists(path):
    os.makedirs(path)
filename = os.path.join(path,timestamp + ".csv")

with open(filename, 'wb') as csvfile:
    IMUwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    IMUwriter.writerow(labels)

    # read from the device
    #s = serial.Serial(port='/dev/ttyUSBserial-A7027EKU', baudrate=38400)
    s = serial.Serial(port='/dev/ttyUSB0', baudrate=38400)


    i = 0

    


    while i!=numsamples:
        print "A: ", i
        i += 1
        readLine =  s.readline()
        parsed = parseData(readLine)
        xaccel = int(parsed[3])
        yaccel = int(parsed[4])
        yaw = int(parsed[2])
        IMUwriter.writerow(parsed)
        print parsed
        #pygame.draw.circle(screen, BLUE, (remap_interval(xaccel), remap_interval(yaccel)), 5, 0)
        #label = myfont.render("G-Force =" + str(math.sqrt((xaccel**2)+(yaccel**2)), 1, (255,255,0)))
        #screen.blit(label, (10, 320))
        #label2 = myfont.render("Yaw = " + str(yaw), 1, (255,255,0))
        #screen.blit(label2, (270, 320))

        xaccel = (float(parsed[3])/ACCEL_CONVERSION)
        yaccel = (float(parsed[4])/ACCEL_CONVERSION)
        
        screen.fill(background_colour)
        pygame.draw.line(screen, GRAY, (remap_interval(-2), remap_interval(0)), (remap_interval(2),remap_interval(0)), 1)
        pygame.draw.line(screen, GRAY, (remap_interval(0), remap_interval(-2)), (remap_interval(0), remap_interval(2)), 1)
        pygame.draw.circle(screen, RED, (175, 175), 170, 1)
        gForce = str('%.2f' % sqrt(xaccel**2 + yaccel**2))
        label = myfont.render("G-Force =" + gForce, 1, (255,255,0))
        screen.blit(label, (10, 320))

        pygame.draw.circle(screen, BLUE,(remap_interval(xaccel), remap_interval(yaccel)), 5, 0)
        # screen.blit(bluecircle, (remap_interval(float(row[3])), remap_interval(float(row[4]))))
        label2 = myfont.render("Yaw = " + str(float(parsed[2])), 1, (255,255,0))
        screen.blit(label2, (270, 320))

        pygame.display.update()
        time.sleep(0.01)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i == numsamples