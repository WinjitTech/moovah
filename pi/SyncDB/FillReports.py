import sqlite3
import MoovahLogger
import time
import datetime
import ConfReader

ReportDBFilePath="/home/pi/Reports/Reports.sqlite"


def InsertIntoDB(strQuery,DBFilePath):

    try:
        NoOfAttempts=10

        con = sqlite3.connect(DBFilePath)
        c = con.cursor()

        while NoOfAttempts>0:

            NoOfAttempts-=1
            try:
                c.execute(strQuery)
                con.commit()
                print("Record inserted !!")
                break

            except Exception,e:
                time.sleep(5)
                continue

    except Exception,e:
        print str(e)
        MoovahLogger.logger.error("Error in Insert Box reports : "+str(e))

    finally:
        if con:
            con.close()


def InsertIntoBoxStartStoplog(BoxID,Latitude,Longitude,TimeStamp,StartedOnDateTime,StopedOnDateTime):

    try:

        strQuery = "insert into boxstartstoplog(BoxID,Latitude,Longitude,TimeStamp,StartedOnDateTime,StopedOnDateTime) VALUES ("
        strQuery += " " + str(BoxID) + ","
        strQuery += " " + str(Latitude) + ","
        strQuery += " " + str(Longitude) + ","
        strQuery += " '" + str(TimeStamp) + "',"
        strQuery += " '" + str(StartedOnDateTime) + "',"
        strQuery += " '" + str(StopedOnDateTime) + "')"

        InsertIntoDB(strQuery,ReportDBFilePath)


    except Exception,e:
        print str(e)

def InsertIntoboxstatusinfolog(BoxID,Latitude,Longitude,TimeStamp,
                               IsDeviceWorking,
                               SizeOfSDCard,
                               UsedOfSDCard,
                               FreeSpaceOnSDCard,
                               SizeOfPenDrive,
                               UsedOfPenDrive,
                               FreeSpaceOnPenDrive,
                               IsPenDriveMountedProperly,
                               IsInternetWorking,
                               IsWifiAdapterWorking,
                               AndroidBuildVersion,
                               BlackberryBuildVersion,
                               DeviceErrorDetails,
                               NoOfConnectedUsers,
                               ConnectedUserIDs):

    try:

        strQuery = "insert into boxstatusinfolog(BoxID,Latitude,Longitude,TimeStamp," \
                   "IsDeviceWorking,SizeOfSDCard,UsedOfSDCard,FreeSpaceOnSDCard,SizeOfPenDrive,UsedOfPenDrive" \
                   ",FreeSpaceOnPenDrive,IsPenDriveMountedProperly,IsInternetWorking,IsWifiAdapterWorking" \
                   ",AndroidBuildVersion,BlackberryBuildVersion,DeviceErrorDetails,NoOfConnectedUsers," \
                   "ConnectedUserIDs) VALUES ("

        strQuery += " " + str(BoxID) + ","
        strQuery += " " + str(Latitude) + ","
        strQuery += " " + str(Longitude) + ","
        strQuery += " '" + str(TimeStamp) + "',"
        strQuery += " " + str(IsDeviceWorking) + ","
        strQuery += " " + str(SizeOfSDCard) + ","
        strQuery += " " + str(UsedOfSDCard) + ","
        strQuery += " " + str(FreeSpaceOnSDCard) + ","
        strQuery += " " + str(SizeOfPenDrive) + ","
        strQuery += " " + str(UsedOfPenDrive) + ","
        strQuery += " " + str(FreeSpaceOnPenDrive) + ","
        strQuery += " " + str(IsPenDriveMountedProperly) + ","
        strQuery += " " + str(IsInternetWorking) + ","
        strQuery += " " + str(IsWifiAdapterWorking) + ","
        strQuery += " '" + str(AndroidBuildVersion) + "',"
        strQuery += " '" + str(BlackberryBuildVersion) + "',"
        strQuery += " '" + str(DeviceErrorDetails) + "',"
        strQuery += " " + str(NoOfConnectedUsers) + ","
        strQuery += " '" + str(ConnectedUserIDs) + "')"

        print str(strQuery)

        InsertIntoDB(strQuery,ReportDBFilePath)

    except Exception,e:
        print str(e)


def InsertIntoboxsyncdatalog(  DateTimeSyncStarted,
                               DateTimeSyncStoped,
                               IsSyncCompletedSuccessfully,
                               SyncErrorDetails):
    try:

        Latitude=0
        Longitude=0
        d = datetime.datetime.now()
        TimeStamp = d.strftime('%Y-%m-%d %H:%M:%S')

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()
        strQuery ="SELECT BoxID FROM box;"
        c.execute(strQuery)
        BoxID=0
        for record in c.fetchall():
            BoxID = record[0]
            break

        if db:
            db.close()

        strQuery = "insert into boxsyncdatalog(BoxID,Latitude,Longitude,TimeStamp,DateTimeSyncStarted,DateTimeSyncStoped,IsSyncCompletedSuccessfully,SyncErrorDetails) VALUES ("
        strQuery += " " + str(BoxID) + ","
        strQuery += " " + str(Latitude) + ","
        strQuery += " " + str(Longitude) + ","
        strQuery += " '" + str(TimeStamp) + "',"
        strQuery += " '" + str(DateTimeSyncStarted) + "',"
        strQuery += " '" + str(DateTimeSyncStoped) + "',"
        strQuery += " " + str(IsSyncCompletedSuccessfully) + ","
        strQuery += " '" + str(SyncErrorDetails) + "')"

        InsertIntoDB(strQuery,ReportDBFilePath)

    except Exception,e:
        print str(e)


def InsertIntoboxsyncdetailslog(ContentURL,
                               IsContentDownloaded,
                               ContentDownloadErrorDetails,
                               ReferenceID,
                               ModuleID):
    try:

        Latitude=0
        Longitude=0
        d = datetime.datetime.now()
        TimeStamp = d.strftime('%Y-%m-%d %H:%M:%S')

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()
        strQuery ="SELECT BoxID FROM box;"
        c.execute(strQuery)
        BoxID=0
        for record in c.fetchall():
            BoxID = record[0]
            break

        if db:
            db.close()

        SyncID = GetMaxRecordCountForSyncDataLog()

        strQuery = "insert into boxsyncdetailslog(BoxID,Latitude,Longitude,TimeStamp," \
                   "SyncID," \
                   "ContentURL," \
                   "IsContentDownloaded," \
                   "ContentDownloadErrorDetails," \
                   "ReferenceID," \
                   "ModuleID) VALUES ("

        strQuery += " " + str(BoxID) + ","
        strQuery += " " + str(Latitude) + ","
        strQuery += " " + str(Longitude) + ","
        strQuery += " '" + str(TimeStamp) + "',"
        strQuery += " '" + str(SyncID) + "',"
        strQuery += " '" + str(ContentURL) + "',"
        strQuery += " " + str(IsContentDownloaded) + ","
        strQuery += " '" + str(ContentDownloadErrorDetails) + "',"
        strQuery += " " + str(ReferenceID) + ","
        strQuery += " " + str(ModuleID) + ")"

        InsertIntoDB(strQuery,ReportDBFilePath)

    except Exception,e:
        print str(e)



def GetMaxRecordCountForSyncDataLog():

    try:
        con = sqlite3.connect(ReportDBFilePath)
        c = con.cursor()
        strQuery ="select Max(SyncID) from boxsyncdatalog;"
        c.execute(strQuery)
        MaxID=0
        for record in c.fetchall():
            MaxID = record[0]
            break

        if con:
            con.close()

        if (MaxID is None) or (MaxID == 0):
            d = datetime.datetime.now()
            TimeStamp = d.strftime('%Y-%m-%d %H:%M:%S')
            InsertIntoboxsyncdatalog(TimeStamp,'',0,'')
            GetMaxRecordCountForSyncDataLog()
        else:
            return MaxID

    except Exception,e:
        return 0