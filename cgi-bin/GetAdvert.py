#!/usr/bin/python

import cgi
import json
import sqlite3
import ConfReader
import sqliteUtilities


form = cgi.FieldStorage()

lastSyncDateTime = (form.getvalue('lastSyncDateTime'))

#lastSyncDateTime= "0001-01-01 00:00:00.000" #datetime.datetime.now()

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""

print "Content-type: application/json\n\n"


try:
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    db = sqlite3.connect(ConfReader.GetSyncDBPath())

    db.row_factory = sqliteUtilities.dict_factory

    c = db.cursor()

#    c.execute("select * from Adverts where ModifiedDate > '" + (lastSyncDateTime) + "' and isRingFence=0;")
    c.execute("select Id ,Title ,AdvertPath ,ThumbnailPath ,SponsorImage ,SponsorLink ,Preferences ,MediaID ,ValidFrom ,ValidTill ,DurationInSeconds ,CreditPoint,URL ,IsGeneral,IsWatched bool  ,IsActive,ModifiedDate ,pointsEarned,IsGPS,GPSLocations ,Radius,IsBoxData,LocalPath ,VisitedID,IsViewLimitReached,Price from Adverts where ModifiedDate > '" + (lastSyncDateTime) + "' and isRingFence=0;")
    results = c.fetchall()

    for result in results:
        strQuery = "select * from AdvertMapping where AdvertID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['AdvertMapping'] = results2

    response['ReturnObject'] = results

    print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
        response = {'result': str(e)}

#print json.JSONEncoder().encode(response)

