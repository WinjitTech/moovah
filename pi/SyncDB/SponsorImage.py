import json
import urllib2
import sqlite3
import sys
import getopt
import FileMgr
import ConfReader
import MoovahLogger


def GetSponsorImages():
    try:

        db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
        db.isolation_level = None
        c = db.cursor()

        c.execute("SELECT BoxID from Box;");

        BoxID = 41
        for record in c.fetchall():
            BoxID = record[0]

        print BoxID
        # BoxID=-1
        url = ConfReader.GetAPIURLCom() + "GetBoxSponsor" + "/" + str(BoxID)
        print url
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')

        # if DataUsed > 0:
        response = urllib2.urlopen(req)
        js = json.load(response)
        # print js
        if js['StatusCode'] == 200:
            c.execute("delete from generalSettings")
            if js['ReturnObject'] == None or js['ReturnObject'] == '':
                print("Sponsor Images not associated with box")
                MoovahLogger.logger.info("Sponsor Images not associated with box")
            else:
                i = 0
                for data in js['ReturnObject']:
                    SponsorImage = str(js['ReturnObject'][i]["SponsorImage"])
                    # print SponsorImage
                    strQuery = "insert into generalSettings(Id,Name,Instructions,IsEarnMoreSponsor,SponsorURL,SponsorImage,IsActive) values('" + str(
                        js['ReturnObject'][i]['Id']) + "','" + str(js['ReturnObject'][i]['Name']) + "','" + str(
                        js['ReturnObject'][i]['Instructions']) + "','" + str(
                        js['ReturnObject'][i]['IsEarnMoreSponsor']) + "','" + str(
                        js['ReturnObject'][i]['SponsorURL']) + "','" + str(
                        js['ReturnObject'][i]["SponsorImage"]) + "',1)"
                    c.execute(strQuery);
                    i = i + 1

                    FileMgr.CheckAndDownloadFile('SponsorImage', SponsorImage, 15, 0)

                    SponsorImage = SponsorImage.replace('small.png', 'medium.png')
                    FileMgr.CheckAndDownloadFile('SponsorImage', SponsorImage, 15, 0)

                    SponsorImage = SponsorImage.replace('medium.png', 'large.png')
                    FileMgr.CheckAndDownloadFile('SponsorImage', SponsorImage, 15, 0)

                MoovahLogger.logger.info("Sponsor Images updated successfully")

    except Exception, e:
        print str(e)

    finally:
        db.close()


GetSponsorImages()
