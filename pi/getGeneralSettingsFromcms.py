import json
import urllib2
import sqlite3
import Schedular
import ConfReader
import MoovahLogger
import datetime
import FileMgr

def main():

    try:     

        IsSchedularStoped=0

        LiveAPIURL = "http://moovahapp.com/Live/LiveAPI/"


        apiurl =ConfReader.GetAPIURLCom() +"GetGeneralSettings/0001-01-01%2000:00:00.000"

        j = urllib2.urlopen(apiurl)    
        js = json.load(j)
        UpgradeTime = js['ReturnObject'][0]['UpgradeTime']
        SyncInterval = js['ReturnObject'][0]['SyncInterval']
        AndroidBuild = js['ReturnObject'][0]['AndroidBuild']
        BlackBerryBuild = js['ReturnObject'][0]['BlackBerryBuild']
        AndroidVersion = js['ReturnObject'][0]['AndroidVersion']
        BlackBerryVersion = js['ReturnObject'][0]['BlackBerryVersion']

        pt =datetime.datetime.strptime(SyncInterval,'%H:%M:%S')
        Sync_Seconds = pt.second+pt.minute*60+pt.hour*3600

        UpgradeDate = datetime.datetime.now().date()
        UpgradeTime = datetime.datetime.strptime(UpgradeTime,'%H:%M:%S')

        UpgradeDateTime = datetime.datetime.combine(UpgradeDate, UpgradeTime.time())

        UpgradeDateTime = datetime.datetime.strptime(str(UpgradeDateTime)+".120000","%Y-%m-%d %H:%M:%S.%f")

        Schedular.StopSchedular()
        IsSchedularStoped=1

        db = sqlite3.connect("/home/pi/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()


        # SyncBox.py
        #c.execute("delete from schedule where Command like '%SyncBox.py%'")                                                                                                                     #values('python /home/pi/AutoUpdate/getGeneralSettingsFromcms.py','2015-03-18 12:38:43.852425',1,3,360,1)
        c.execute("update schedule set Interval='"+str(Sync_Seconds)+"' where Command like '%update.py%'")

        # upgrade.py
        #c.execute("delete from schedule where Command like '%upgrade.py%'")                                                                                                                     #values('python /home/pi/AutoUpdate/getGeneralSettingsFromcms.py','2015-03-18 12:38:43.852425',1,3,360,1)
        c.execute("update schedule set DateTime='"+str(UpgradeDateTime)+"' where Command like '%upgrade.py%'")


        c.execute("SELECT AndroidBuild,BlackBerryBuild,AndroidVersion,BlackBerryVersion from generalSettings;");
        AndroidBuildLocal=""
        BlackBerryBuildLocal =""
        AndroidVersionLocal =""
        BlackBerryVersionLocal =""
        for record in c:
            AndroidBuildLocal=record[0]
            BlackBerryBuildLocal =record[1]
            AndroidVersionLocal =record[2]
            BlackBerryVersionLocal =record[3]

        #AndroidBuild

        if AndroidVersion != AndroidVersionLocal:

            if AndroidBuildLocal is None or AndroidBuildLocal is '':
                AndroidBuildLocal = "/var/www/moovah/Apps/android/moovah.apk"

            FileMgr.DownloadFileToPath(AndroidBuild,AndroidBuildLocal)
            Schedular.runCommand("chmod 777 -R "+AndroidBuildLocal,1)
            c.execute("update generalSettings set AndroidVersion='"+str(AndroidVersion)+"'")
        else:
            MoovahLogger.logger.debug("Android Version "+str(AndroidVersionLocal) +" is already present on Box.")


        #BlackBerryBuild

        if BlackBerryVersion != BlackBerryVersionLocal:

            if BlackBerryBuildLocal is None or BlackBerryBuildLocal is '':
                BlackBerryBuildLocal = "/var/www/moovah/Apps/blackberry/"

            FileMgr.DownloadFileToPath(BlackBerryBuild,BlackBerryBuildLocal+"moovah.zip")

            Schedular.runCommand("unzip "+BlackBerryBuildLocal+"moovah.zip"+" -d "+BlackBerryBuildLocal,1)
            Schedular.runCommand("chmod 777 -R "+BlackBerryBuildLocal,1)
            c.execute("update generalSettings set BlackBerryVersion='"+str(BlackBerryVersion)+"'")
        else:
            MoovahLogger.logger.debug("Blackberry Version "+str(BlackBerryVersionLocal) +" is already present on Box.")

        db.commit()

    except Exception,e:
        MoovahLogger.logger.error("Error in getGeneralSettingsFromcms Process: "+str(e))

    finally:
        if IsSchedularStoped==1:
            Schedular.StartSchedular()
            IsSchedularStoped=0


if __name__ == "__main__":
    main()
