import urllib2
import time
import subprocess
import RPi.GPIO as GPIO              # import RPi.GPIO module
import sys, time
from daemon import Daemon

def internet_on():
    try:
        response=urllib2.urlopen('http://168.63.241.212',timeout=20)
        return True
    except urllib2.URLError as err: pass
    return False

def TestUSBMounting():
    mounts = {}
    for line in subprocess.check_output(['mount', '-l']).split('\n'):
        parts = line.split(' ')
        if len(parts) > 2:
            mounts[parts[0]] = parts[2]

    if '/dev/sda1' in mounts.keys():
        if mounts['/dev/sda1'] == '/media/usb0':
            return True
    print(mounts['/dev/sda1'])
    return False


def RunGPIO():

    # choose BOARD or BCM
    #GPIO.setmode(GPIO.BCM)               # BCM for GPIO numbering
    GPIO.setmode(GPIO.BOARD)             # BOARD for P1 pin numbering

    # Set up Outputs
    GPIO.setup(7, GPIO.OUT, initial=0)    # set initial value option (1 or 0)
    GPIO.setup(13, GPIO.OUT, initial=0)    # set initial value option (1 or 0)


    while True:

        GPIO.output(7, 0)
        GPIO.output(13, 0)


        if internet_on():
        # Switch Outputs
            GPIO.output(7, 1)
            print "internet On"

        if TestUSBMounting():
        # Switch Outputs
            GPIO.output(13, 1)
            print "USB Connected"

        time.sleep(1)
         # delays for 5 seconds

class MyDaemon(Daemon):
    def run(self):
        while True:

            GPIO.output(7, 0)
            GPIO.output(13, 0)


            if internet_on():
            # Switch Outputs
                GPIO.output(7, 1)
                print "internet On"

            if TestUSBMounting():
            # Switch Outputs
                GPIO.output(13, 1)
                print "USB Connected"

            time.sleep(1)
             # delays for 5 seconds




GPIO.setmode(GPIO.BOARD)             # BOARD for P1 pin numbering

# Set up Outputs
GPIO.setup(7, GPIO.OUT, initial=0)    # set initial value option (1 or 0)
GPIO.setup(13, GPIO.OUT, initial=0)    # set initial value option (1 or 0)


daemon = MyDaemon('/var/run/daemon-example.pid')

if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
        daemon.start()
    elif 'stop' == sys.argv[1]:
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)
else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)
