#!/usr/bin/python

import json
import urllib2
import sqlite3
import MoovahLogger
import FileMgr
import Schedular
import datetime
import os
import ConfReader

def StartUpgradeProcess():

    try:


        #Step 1: Get BoxID,BoxVersion,UpgradeZipLocalPath,UpgradeLocalPath from data.db

        db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
        db.isolation_level=None
        c = db.cursor()

        c.execute("SELECT LiveAPIURL,BoxVersion,UpgradeLocalPath,UpgradeZipLocalPath from upgradeSettings;");

        BoxVersion ="1.0"
        UpgradeLocalPath =""
        UpgradeZipLocalPath =""
        for record in c.fetchall():
            LiveAPIURL = record[0]
            BoxVersion = record[1]
            UpgradeLocalPath = record[2]
            UpgradeZipLocalPath = record[3]
	


        MoovahLogger.logger.debug("Upgrade path: "+str(UpgradeLocalPath))
        #Delete all UnCompressed Files
        Schedular.runCommand("rm -rf "+UpgradeLocalPath+"*",1)

        if os.path.exists(UpgradeZipLocalPath):
            Schedular.runCommand("rm -f "+UpgradeZipLocalPath,1)

        c.execute("SELECT BoxID from Box;");

        BoxID=43
        for record in c.fetchall():
            BoxID = record[0]
	
        if ( (BoxID is  None) or (BoxID is '')):
            BoxID=41

        if ((BoxVersion is None) or (BoxVersion is '')):
            BoxVersion='0.00'

        c.execute("insert into upgradelog(BoxID,BoxVersion,IsUpgradeStarted,DateTime) values("+str(BoxID)+","+str(BoxVersion)+",1,'"+str(datetime.datetime.now())+"');");

        #Close database
        db.close()

        #Step 2: Get Update version from CMS

        apiurl =ConfReader.GetAPIURLCom() +"GetBoxVersionNew/"+ str(BoxID)


        j = urllib2.urlopen(apiurl)
        js = json.load(j)
        GlobalPath = js['ReturnObject'][0]['GlobalPath']
        BoxSpecificPath = js['ReturnObject'][0]['BoxSpecificPath']
        IsBoxSpecificUpgrade = js['ReturnObject'][0]['IsBoxSpecificUpgrade']
        GlobalVersion = js['ReturnObject'][0]['GlobalVersion']

	print IsBoxSpecificUpgrade
        if str(IsBoxSpecificUpgrade).lower() == "false" and ((GlobalVersion is None) or (GlobalVersion is '')):
            MoovahLogger.logger.info("GlobalVersion is "+str(GlobalVersion) + " upgrade process will terminate now.")
            return

        #Step 3. Check for Box Version and GlobalVersion

        if str(IsBoxSpecificUpgrade).lower() == "false" and float(BoxVersion)>=float(GlobalVersion):
            MoovahLogger.logger.info("Box is already having latest version, BoxVersion is "+str(BoxVersion) + "and GlobalVersion is "+str(GlobalVersion))
	    print ("Box is already having latest version, BoxVersion is "+str(BoxVersion) + " and GlobalVersion is "+str(GlobalVersion))
            #Step 10:
            #Give call to LiveAPI about upgrade process is finished

            apiurl =ConfReader.GetAPIURLCom() +"UpdateBoxVersion"
            postdata = {"BoxID": BoxID,"BoxVersion": BoxVersion,"IsBoxSpecificUpgrade": False}
	    
            req = urllib2.Request(apiurl)
            req.add_header('Content-Type','application/json')
	    data = json.dumps(postdata)
            
            response = urllib2.urlopen(req,data)

            return

        ######### New Code added for Box Specific upgrade #######
        ######### Box Specific Code Start #######

        if str(IsBoxSpecificUpgrade).lower() == "true" and ((BoxSpecificPath is not None) or (BoxSpecificPath is not '')):
	   
            print str(IsBoxSpecificUpgrade)
            print BoxSpecificPath
            print UpgradeZipLocalPath

            DownloadStatus = FileMgr.DownloadFileToPath(BoxSpecificPath,UpgradeZipLocalPath)

            print "DownloadStatus"+str(DownloadStatus)

	    apiurl =ConfReader.GetAPIURLCom() +"UpdateBoxVersion"
	    
            postdata = {"BoxID": BoxID,"BoxVersion": GlobalVersion,"IsBoxSpecificUpgrade": True}
            print postdata
            req = urllib2.Request(apiurl)
            req.add_header('Content-Type','application/json')
            data = json.dumps(postdata)
	    response = urllib2.urlopen(req,data)

            MoovahLogger.logger.info("Box specific upgrade successful.")
        else:

        ######### Box Specific Code End #######

            if (GlobalPath is None or GlobalPath is ''):
                MoovahLogger.logger.info("Global upgrade path is emtry, upgrade process will now stop.")
                return
            else:

                FileMgr.DownloadFileToPath(GlobalPath,UpgradeZipLocalPath)
                MoovahLogger.logger.info("Global upgrade in process.")


        #Step 4:
        #Create folder and unzip files to local folder.
        Schedular.runCommand("mkdir -p "+UpgradeLocalPath,1)
        Schedular.runCommand("unzip -o "+UpgradeZipLocalPath+" -d "+UpgradeLocalPath,1)
        Schedular.runCommand("chmod 777 -R "+UpgradeLocalPath,1)


        #Step 5:
        #Check for AutoUpdate.sqlite file in UpgradeLocalPath files:
        #If not present stop upgrade process

        if not os.path.exists(UpgradeLocalPath+"Autoupdate.sqlite"):
            MoovahLogger.logger.info("Autoupdate.sqlite file is not present in upgrade.zip file root location, upgrade will now terminate.")
            return


        #Step 6:
        #Connect to AutoUpdate.sqlite db and start Upgrade process

        db = sqlite3.connect(UpgradeLocalPath+"Autoupdate.sqlite")
        db.isolation_level=None
        c = db.cursor()

        #Step 7:
        #Copy all files from Autoupdate.sqlite database

        c.execute("SELECT LocalSrcPath,LocalDstPath from files;");
        LocalSrcPath=""
        LocalDstPath =""
        for record in c.fetchall():
            LocalSrcPath=record[0]
            LocalDstPath =record[1]

            FileMgr.copyAllFilesToDir(LocalSrcPath,LocalDstPath)

        #Step 8:
        #Run all the commands from Autoupdate.sqlite database

        c.execute("SELECT command,IsSudo from commands;");
        command=""
        IsSudo =""
        for record in c.fetchall():
            command=record[0]
            IsSudo =record[1]

            Schedular.runCommand(command,IsSudo)


        #Close database AutoUpddate.sqlite
        db.close()


        #Step 9:
        #Write upgrade status back to data.db

        db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
        db.isolation_level=None
        c = db.cursor()

        strQuery ="insert into upgradelog(BoxID,BoxVersion,IsUpgradeDone,DateTime) values("+str(BoxID)+",'"+str(GlobalVersion)+"',1,'"+str(datetime.datetime.now())+"');"
        MoovahLogger.logger.info(strQuery)
        c.execute(strQuery)

        strQuery = "update upgradeSettings SET BoxVersion= '"+str(GlobalVersion)+"';"
        MoovahLogger.logger.info(strQuery)
        c.execute(strQuery)

        db.commit()

        #Close database data.db
        db.close()


        #Delete all UnCompressed Files
        Schedular.runCommand("rm -r "+UpgradeLocalPath+"*",1)
        Schedular.runCommand("rm -f "+UpgradeZipLocalPath,1)

        #Step 10:
        #Give call to LiveAPI about upgrade process is finished

        apiurl =ConfReader.GetAPIURLCom() +"UpdateBoxVersion"
        postdata = {"BoxID": BoxID,"BoxVersion": GlobalVersion,"IsBoxSpecificUpgrade": False}
	print postdata
        req = urllib2.Request(apiurl)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)

	print data

        response = urllib2.urlopen(req,data)
	print response
        MoovahLogger.logger.info("Box Upgraded to "+str(GlobalVersion) + " successfully")


    except Exception,e:
        MoovahLogger.logger.error("Error in Upgrade Process: "+str(e))

StartUpgradeProcess()
