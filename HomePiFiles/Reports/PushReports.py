import json
import urllib2
import sqlite3
import MoovahLogger
import time
import ConfReader
import getopt
import sys
import BoxStatusInfoLog

ReportDBFilePath="/home/pi/Reports/Reports.sqlite"


def PushBoxStartStoplog():

    db = sqlite3.connect(ReportDBFilePath)
    c = db.cursor()

    PostData ={}

    c.execute("SELECT BoxID,Latitude,Longitude,TimeStamp,StartedOnDateTime,StopedOnDateTime FROM boxstartstoplog;")

    i=0

    for record in c.fetchall():

        BoxID = record[0]
        Latitude = record[1]
        Longitude = record[2]
        TimeStamp = record[3]
        StartedOnDateTime = record[4]
        StopedOnDateTime = record[5]

        PostData[i]={ "BoxID":BoxID ,"Latitude":Latitude,
                      "Longitude":Longitude,"TimeStamp":TimeStamp,"StartedOnDateTime":StartedOnDateTime,
                      "StopedOnDateTime":StopedOnDateTime}
        i+=1

    db.close()

    try:

        if i>0:

            url = ConfReader.GetAPIURLCom() +"SaveBoxStartStopLog"

            print url

            postdata = PostData.values()

            print postdata

            req = urllib2.Request(url)
            req.add_header('Content-Type','application/json')
            data = json.dumps(postdata)

            #if DataUsed > 0:
            response = urllib2.urlopen(req,data)
            js = json.load(response)
            print js
            if js['StatusCode'] == 200:

                db = sqlite3.connect(ReportDBFilePath)
                c = db.cursor()

                c.execute("delete from boxstartstoplog")
                db.commit()
                db.close()
                MoovahLogger.logger.info("Records pushed to CMS from PushBoxStartStoplog.")

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Records pushed to CMS from PushBoxStartStoplog.")



def Pushboxstatusinfolog():

    BoxStatusInfoLog.FillRecords()

    db = sqlite3.connect(ReportDBFilePath)
    c = db.cursor()

    PostData ={}

    c.execute("SELECT BoxID,Latitude,Longitude,TimeStamp,IsDeviceWorking,SizeOfSDCard,"
              "UsedOfSDCard,FreeSpaceOnSDCard,SizeOfPenDrive,UsedOfPenDrive,FreeSpaceOnPenDrive"
              ",IsPenDriveMountedProperly,IsInternetWorking,IsWifiAdapterWorking,AndroidBuildVersion,"
              "BlackberryBuildVersion,DeviceErrorDetails,NoOfConnectedUsers,ConnectedUserIDs FROM BoxStatusInfoLog;")

    i=0

    for record in c.fetchall():

        BoxID = record[0]
        Latitude = record[1]
        Longitude = record[2]
        TimeStamp = record[3]
        IsDeviceWorking = record[4]
        SizeOfSDCard = record[5]
        UsedOfSDCard = record[6]
        FreeSpaceOnSDCard = record[7]
        SizeOfPenDrive = record[8]
        UsedOfPenDrive = record[9]
        FreeSpaceOnPenDrive = record[10]
        IsPenDriveMountedProperly = record[11]
        IsInternetWorking = record[12]
        IsWifiAdapterWorking = record[13]
        AndroidBuildVersion = record[14]
        BlackberryBuildVersion = record[15]
        DeviceErrorDetails = record[16]
        NoOfConnectedUsers = record[17]
        ConnectedUserIDs = record[18]

        PostData[i]={ "BoxID":BoxID ,"Latitude":Latitude,
                      "Longitude":Longitude,"TimeStamp":TimeStamp,"IsDeviceWorking":IsDeviceWorking,
                      "SizeOfSDCard":SizeOfSDCard,
                      "UsedOfSDCard":UsedOfSDCard,
                      "FreeSpaceOnSDCard":FreeSpaceOnSDCard,
                      "SizeOfPenDrive":SizeOfPenDrive,
                      "UsedOfPenDrive":UsedOfPenDrive,
                      "FreeSpaceOnPenDrive":FreeSpaceOnPenDrive,
                      "IsPenDriveMountedProperly":IsPenDriveMountedProperly,
                      "IsInternetWorking":IsInternetWorking,
                      "IsWifiAdapterWorking":IsWifiAdapterWorking,
                      "AndroidBuildVersion":AndroidBuildVersion,
                      "BlackberryBuildVersion":BlackberryBuildVersion,
                      "DeviceErrorDetails":DeviceErrorDetails,
                      "NoOfConnectedUsers":NoOfConnectedUsers,
                      "ConnectedUserIDs":ConnectedUserIDs
                      }
        i+=1

    db.close()

    try:
        if i>0:
            url = ConfReader.GetAPIURLCom() +"SaveBoxStatusInfoLog"

            print url

            postdata = PostData.values()

            print postdata

            req = urllib2.Request(url)
            req.add_header('Content-Type','application/json')
            data = json.dumps(postdata)

            #if DataUsed > 0:
            response = urllib2.urlopen(req,data)
            js = json.load(response)
            print js

            if js['StatusCode'] == 200:

                db = sqlite3.connect(ReportDBFilePath)
                c = db.cursor()

                c.execute("delete from BoxStatusInfoLog")
                db.commit()
                db.close()

                MoovahLogger.logger.info("Records pushed to CMS from Pushboxstatusinfolog.")

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Error in Pushboxstatusinfolog: "+str(e))


def Pushboxsyncdatalog():

    db = sqlite3.connect(ReportDBFilePath)
    c = db.cursor()

    PostData =""

    c.execute("SELECT SyncID,BoxID,Latitude,Longitude,TimeStamp,DateTimeSyncStarted,DateTimeSyncStoped,IsSyncCompletedSuccessfully"
              ",SyncErrorDetails FROM BoxSyncDataLog;")

    i=0
    for record in c.fetchall():

        SyncID = record[0]
        BoxID = record[1]
        Latitude = record[2]
        Longitude = record[3]
        TimeStamp = record[4]
        DateTimeSyncStarted = record[5]
        DateTimeSyncStoped = record[6]
        IsSyncCompletedSuccessfully = record[7]
        SyncErrorDetails = record[8]

        PostData={  "SyncID":SyncID,"BoxID":BoxID ,"Latitude":Latitude,
                      "Longitude":Longitude,"TimeStamp":TimeStamp,"DateTimeSyncStarted":DateTimeSyncStarted,
                      "DateTimeSyncStoped":DateTimeSyncStoped,
                      "IsSyncCompletedSuccessfully":IsSyncCompletedSuccessfully,
                      "SyncErrorDetails":SyncErrorDetails
                }
        i+=1
        break;

    db.close()

    try:
        if i>0:

            url = ConfReader.GetAPIURLCom() +"SaveBoxSyncDataLog"

            print url

            postdata = PostData

            print postdata

            req = urllib2.Request(url)
            req.add_header('Content-Type','application/json')
            data = json.dumps(postdata)

            #if DataUsed > 0:
            response = urllib2.urlopen(req,data)
            js = json.load(response)
            print js

            if js['StatusCode'] == 200:

                db = sqlite3.connect(ReportDBFilePath)
                c = db.cursor()

                c.execute("delete from BoxSyncDataLog")
                db.commit()
                db.close()
                MoovahLogger.logger.info("Records pushed to CMS from Pushboxsyncdatalog.")

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Error in Pushboxsyncdatalog: "+str(e))



def PushBoxSyncDetailsLog():

    db = sqlite3.connect(ReportDBFilePath)
    c = db.cursor()

    PostData ={}

    c.execute("SELECT SyncID,BoxID,Latitude,Longitude,TimeStamp,ContentURL,IsContentDownloaded,ContentDownloadErrorDetails"
              ",ReferenceID,ContentSizeInBytes,ModuleID FROM boxsyncdetailslog;")

    i=0
    for record in c.fetchall():

        SyncID = record[0]
        BoxID = record[1]
        Latitude = record[2]
        Longitude = record[3]
        TimeStamp = record[4]
        ContentURL = record[5]
        IsContentDownloaded = record[6]
        ContentDownloadErrorDetails = record[7]
        ReferenceID = record[8]
        ContentSizeInBytes = record[9]
        ModuleID = record[10]

        PostData[i]={ "SyncID":SyncID, "BoxID":BoxID ,"Latitude":Latitude,
                      "Longitude":Longitude,"TimeStamp":TimeStamp,"ContentURL":ContentURL,
                      "IsContentDownloaded":IsContentDownloaded,
                      "ContentDownloadErrorDetails":ContentDownloadErrorDetails,
                      "ReferenceID":ReferenceID,
                      "ContentSizeInBytes":ContentSizeInBytes,
                      "ModuleID":ModuleID
                      }
        i+=1

    db.close()

    try:
        if i>0:

            url = ConfReader.GetAPIURLCom() +"SaveBoxSyncDetailsLog"

            print url

            postdata = PostData.values()

            print postdata

            req = urllib2.Request(url)
            req.add_header('Content-Type','application/json')
            data = json.dumps(postdata)

            #if DataUsed > 0:
            response = urllib2.urlopen(req,data)
            js = json.load(response)
            print js

            if js['StatusCode'] == 200:

                db = sqlite3.connect(ReportDBFilePath)
                c = db.cursor()

                c.execute("delete from boxsyncdetailslog")
                db.commit()
                db.close()

                MoovahLogger.logger.info("Records pushed to CMS from PushBoxSyncDetailsLog.")

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Error in PushBoxSyncDetailsLog: "+str(e))



try:

    opts, args = getopt.getopt(sys.argv[1:],'h:',["Report="])
except getopt.GetoptError:
    print 'Usage: PushReports.py --Report=1 '
    sys.exit(2)

ReportName = '2'

for opt, arg in opts:
    if opt == '--Report':
        ReportName = arg

if ReportName is '1':
    PushBoxStartStoplog()
    print 'Pushed BoxStartStoplog to CMS'
elif ReportName is '2':
    Pushboxstatusinfolog()
    print 'Pushed boxstatusinfolog to CMS'
elif ReportName is '3':
    Pushboxsyncdatalog()
    print 'Pushed boxsyncdatalog to CMS'
elif ReportName is '4':
    PushBoxSyncDetailsLog()
    print 'Pushed BoxSyncDetailsLog to CMS'
else:
    print 'Usage: PushReports.py --Report=1'

#PushBoxStartStoplog()
#Pushboxstatusinfolog()
#Pushboxsyncdatalog()
#PushBoxSyncDetailsLog()