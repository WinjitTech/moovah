import urllib2
import sqlite3
import sys
import os
import commands
import platform
import ConfReader
import FillReports
import subprocess
import datetime
import MoovahLogger

def internet_on():
    try:
        response=urllib2.urlopen(ConfReader.GetAPIURLCom(),timeout=20)
        print "Internet Response: "+str(response)
        return 1
    except Exception,e:
        print str(e)
        return str('Internet not available')

def TestUSBMounting():
    mounts = {}
    for line in subprocess.check_output(['mount', '-l']).split('\n'):
        parts = line.split(' ')
        if len(parts) > 2:
            mounts[parts[0]] = parts[2]

    if '/dev/sda1' in mounts.keys():
        if mounts['/dev/sda1'] == '/media/usb0':
            return 1
    print(mounts['/dev/sda1'])
    return 0



def FillRecords():

    try:

        Lattiude=0
        Longitude=0

        a = commands.getoutput("df -k /dev/root")

        #SDCARD = a[49:58]
        lines = a.split("\n")

        CardDetails = lines[1].split()

        print lines[1]

        SizeOfSDCard = CardDetails[1]
        UsedOfSDCard = CardDetails[2]
        FreeSpaceOnSDCard = CardDetails[3]

        b = commands.getoutput("df -k /dev/sda1")

        lines = b.split("\n")

        CardDetails = lines[1].split()

        SizeOfPenDrive = CardDetails[1]
        UsedOfPenDrive = CardDetails[2]
        FreeSpaceOnPenDrive = CardDetails[3]

        ConnectedIPs=""

        ConnectedIPs = commands.getoutput("netstat -tn 2>/dev/null | awk '{print $5}' | cut -d: -f1 | sort | uniq")

        BoxID=0
        NoOfConnectedUsers=0
        UserIDs =""

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()

        for IpAddress in ConnectedIPs.split("\n"):

            userID=None
            strQuery ="SELECT userID FROM Users where IP='"+str(IpAddress)+"';"

            c.execute(strQuery)

            print(databaseFilePath)

            for record in c.fetchall():
                userID = record[0]
                print(str(userID))
                if str(userID) not in UserIDs:
                    UserIDs += str(userID)+','
                    NoOfConnectedUsers+=1
        if db:
            db.close()

        print str("UserIDs: "+ UserIDs)

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()
        strQuery ="SELECT BoxID FROM box;"
        c.execute(strQuery)

        for record in c.fetchall():
            BoxID = record[0]
            break

        if db:
            db.close()

        UserIDs =UserIDs[:-1]

        AndroidBuildVersion =""
        BlackberryBuildVersion =""
        db = sqlite3.connect("/home/pi/AutoUpdate/Schedular.sqlite")
        c = db.cursor()
        c.execute("select AndroidVersion,BlackBerryVersion from generalsettings");
        for record in c.fetchall():
            AndroidBuildVersion = record[0]
            BlackberryBuildVersion = record[1]
            break

        db.close()

        d = datetime.datetime.now()
        TimeStamp = d.strftime('%Y-%m-%d %H:%M:%S')
        IsDeviceWorking=1
        IsPenDriveMountedProperly = TestUSBMounting()

        DeviceErrorDetails=''

        if internet_on() == 1:
            IsInternetWorking = 1
        else:
            IsInternetWorking = 0
            DeviceErrorDetails = internet_on()
        IsWifiAdapterWorking= 1

        FillReports.InsertIntoboxstatusinfolog(BoxID,Lattiude,Longitude,
                                               TimeStamp,IsDeviceWorking,SizeOfSDCard,UsedOfSDCard,FreeSpaceOnSDCard,
                                               SizeOfPenDrive,UsedOfPenDrive,FreeSpaceOnPenDrive,IsPenDriveMountedProperly
                                               ,IsInternetWorking,IsWifiAdapterWorking,AndroidBuildVersion,BlackberryBuildVersion
                                               ,DeviceErrorDetails,NoOfConnectedUsers,UserIDs)

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Error in FillRecords: "+str(e))

FillRecords()