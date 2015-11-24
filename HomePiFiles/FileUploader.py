__author__ = 'Shrikant'
import base64
import urllib2
import json
import GetFileInfo
import time
import ConfReader
import sqlite3

def FileTOBase64ByteArray(path):
    try:
        s = bytearray(open(path, "rb").read())
        # Encode as Base64
        a = base64.b64encode(open(path, "rb").read())
        return a

    except Exception,e:
        print str(e)
        return None


def PostJsonDataToURL(url,postdata):
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)

        #if DataUsed > 0:
        response = urllib2.urlopen(req,data)
        js = json.load(response)
        #print response
        if js['StatusCode'] == 200:
            print "Success :"+str(js['StatusCode'])
        else:
            print "Error while sending :" +str(js['StatusCode'])

    except Exception,e:
        print str(e)


def PostDeviceReportZipToCMS():
    try:

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'

        print databaseFilePath
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()

        BoxID = None
        c.execute("SELECT BoxID FROM Box LIMIT 1;");
        for record in c.fetchall():
          BoxID = record[0]

        url = ConfReader.GetAPIURLCom() +"SaveZip/"+str(BoxID)

        print url

        GetFileInfo.GenerateDeviceReportZip()
        b64ary = FileTOBase64ByteArray("/home/pi/dignostics.tar.gz")

        postdata ={ "ZipBase64String": b64ary,"Timestamp": time.time(),"UploadArea": 3 }

        #print postdata

        PostJsonDataToURL(url,postdata)

    except Exception,e:
        print str(e)


def PostDailyDeviceBackupZipToCMS():
    try:

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'

        print databaseFilePath
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()

        BoxID = None
        c.execute("SELECT BoxID FROM Box LIMIT 1;");
        for record in c.fetchall():
          BoxID = record[0]

        url = ConfReader.GetAPIURLCom() +"SaveZip/"+str(BoxID)

        print url

        GetFileInfo.GenerateDailyDeviceBackupZip()
        b64ary = FileTOBase64ByteArray("/home/pi/bkp.tar")

        postdata ={ "ZipBase64String": b64ary,"Timestamp": time.time(),"UploadArea": 1 }

        #print postdata

        PostJsonDataToURL(url,postdata)

    except Exception,e:
        print str(e)


def PostDeviceBackupZipToCMS():
    try:

        databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'

        print databaseFilePath
        db = sqlite3.connect(databaseFilePath)
        c = db.cursor()

        BoxID = None
        c.execute("SELECT BoxID FROM Box LIMIT 1;");
        for record in c.fetchall():
          BoxID = record[0]

        url = ConfReader.GetAPIURLCom() +"SaveZip/"+str(BoxID)

        print url

        GetFileInfo.GenerateDailyDeviceBackupZip()
        b64ary = FileTOBase64ByteArray("/home/pi/bkp.tar")

        postdata ={ "ZipBase64String": b64ary,"Timestamp": time.time(),"UploadArea": 2 }

        PostJsonDataToURL(url,postdata)

    except Exception,e:
        print str(e)

PostDeviceReportZipToCMS()
PostDailyDeviceBackupZipToCMS()
PostDeviceBackupZipToCMS()