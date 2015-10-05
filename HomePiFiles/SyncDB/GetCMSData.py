import json
import urllib2
import sqlite3
import codecs


import ConfReader


ConsolidatedData=''


def GetDataFromCMS():

    lFile = open("ConsolidatedData.txt", "w+")
    lFile.close()

    db = sqlite3.connect('/home/pi/pythonlogger.py/data.db')
    db.isolation_level=None
    c = db.cursor()

    records = c.execute("SELECT BoxID FROM Box LIMIT 1;");

    for record in c.fetchall():
        BoxID = record[0]


    url = ConfReader.GetAPIURLCom()+"GetBoxData/" #+ str(BoxID)
    postdata = GenerateJsonDataForRequest()
    req = urllib2.Request(url)
    # req.add_header('Pragma','no-cache')
    # req.add_header('Cache-Control','max-age=0, no-cache, no-store, must-revalidate')
    req.add_header('Content-Type','application/json')
    data = json.dumps(postdata)

    response = urllib2.urlopen(req,data)

    js = json.loads(response.read())

    #dataURL = js['ReturnObject'][0]['Message']
    ConsolidatedData = js['ReturnObject'][0]


    with codecs.open("ConsolidatedData.txt", "w","utf-8") as myfile:
            json.dump(ConsolidatedData, myfile)


def GetData(key):

    ConsolidatedData=''
    with codecs.open("ConsolidatedData.txt", "r","utf-8") as myfile:
            js = myfile.read()
            ConsolidatedData = json.loads(js)
    return ConsolidatedData[key]


def GenerateJsonDataForRequest():

    postdata =[]

    db = sqlite3.connect(ConfReader.GetSyncDBPath())
    db.isolation_level=None
    c = db.cursor()

    #Album
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Album order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Albums','LastSyncDateTime':str(lastSyncDateTime)},

    #Apps
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from apps order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Apps','LastSyncDateTime':str(lastSyncDateTime)},


    #Articles
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Article order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Articles','LastSyncDateTime':str(lastSyncDateTime)},


    #NewsFeeds
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from rss order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'NewsFeeds','LastSyncDateTime':str(lastSyncDateTime)},

    #Surveys
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Survey order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Surveys','LastSyncDateTime':str(lastSyncDateTime)},

    #Competitions
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Competition order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Competitions','LastSyncDateTime':str(lastSyncDateTime)},

    #Deals
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Deals order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Deals','LastSyncDateTime':str(lastSyncDateTime)},

    #Categories
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Category order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Categories','LastSyncDateTime':str(lastSyncDateTime)},

    #SubCategories
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from SubCategory order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'SubCategories','LastSyncDateTime':str(lastSyncDateTime)},

    #Preferences
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Preferences order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Preferences','LastSyncDateTime':str(lastSyncDateTime)},

    #Adverts
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Adverts order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Adverts','LastSyncDateTime':str(lastSyncDateTime)},

    # #BannerImages
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    postdata += {'Key':'BannerImages','LastSyncDateTime':str(lastSyncDateTime)},

    #Box
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Box order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Box','LastSyncDateTime':str(lastSyncDateTime)},


    #Sponsors
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Sponsor order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Sponsors','LastSyncDateTime':str(lastSyncDateTime)},


    #Retailers
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Retailer order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Retailers','LastSyncDateTime':str(lastSyncDateTime)},


    #Routes
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from Route order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'Routes','LastSyncDateTime':str(lastSyncDateTime)},



    #ContentOwners
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from ContentOwner order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'ContentOwners','LastSyncDateTime':str(lastSyncDateTime)},


    #CreditRules
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from CreditRule order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'CreditRules','LastSyncDateTime':str(lastSyncDateTime)},


    #TermsAndConditions
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from TermsAndConditions order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'TermsAndConditions','LastSyncDateTime':str(lastSyncDateTime)},

    #GeneralSettings
    lastSyncDateTime=  "0001-01-01%2000:00:00.000" #datetime.datetime.now()
    c.execute('select ModifiedDate from GeneralSetting order by ModifiedDate desc LIMIT 1')
    for record in c.fetchall():
        lastSyncDateTime = record[0]

    postdata += {'Key':'GeneralSettings','LastSyncDateTime':str(lastSyncDateTime)},


    return postdata

def CleanDatabaseFile():

    print ConfReader.GetSyncDBPath()

    db = sqlite3.connect(ConfReader.GetSyncDBPath())
    db.isolation_level=None
    c = db.cursor()

    cmds = c.execute("select 'delete from ' || name || ';' from sqlite_master where type = 'table';")

    for cmd in cmds.fetchall():
        cmd = str(cmd)[3:-3]
        if not 'sqlite_sequence' in cmd:
            c.execute(cmd)

    db.commit()
