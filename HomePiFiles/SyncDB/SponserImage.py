import json
import urllib2
import sqlite3
import sys
import getopt
import FileMgr
import ConfReader
import MoovahLogger

def main():

    try:

        db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
        db.isolation_level=None
        c = db.cursor()

        c.execute("SELECT BoxID from Box;");

        BoxID=41
        for record in c.fetchall():
            BoxID = record[0]

        url = ConfReader.GetAPIURLCom() +"GetBoxSponsor"+"/"+str(BoxID)

        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')

        #if DataUsed > 0:
        response = urllib2.urlopen(req)
        js = json.load(response)
        #print response
        if js['StatusCode'] == 200:

            SponsorURL = str(js['ReturnObject'][0]["SponsorURL"])
            SponsorImage = str(js['ReturnObject'][0]["SponsorImage"])

            c.execute("delete from generalSettings where key='SponsorURL' or key='SponsorImage' ;");
            c.execute("insert into generalSettings(key,value,IsActive) values('SponsorURL','"+SponsorURL+"',1)");
            c.execute("insert into generalSettings(key,value,IsActive) values('SponsorImage','"+SponsorImage+"',1)");

            FileMgr.CheckAndDownloadFile('SponsorImage',SponsorImage,15,0)

            SponsorImage = SponsorImage.replace('small.png','medium.png')
            FileMgr.CheckAndDownloadFile('SponsorImage',SponsorImage,15,0)

            SponsorImage = SponsorImage.replace('medium.png','large.png')
            FileMgr.CheckAndDownloadFile('SponsorImage',SponsorImage,15,0)

    except Exception, e:
        print str(e)

    finally:
        db.close()

if __name__ == "__main__":
    main()

MoovahLogger.logger.info("Sponsor Images updated successfully")