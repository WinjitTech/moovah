#!/usr/bin/python

import cgi
import json
import sqlite3

import sqliteUtilities
import ConfReader

form = cgi.FieldStorage()

lastSyncDateTime = (form.getvalue('lastSyncDateTime'))
platformID = (form.getvalue('platformID'))
platformID = 1

lastSyncDateTime= "0001-01-01 00:00:00.000" #datetime.datetime.now()

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""
response['NextPageLink']=""+str(platformID)+""



print "Content-type: application/json\n\n"


try:
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    db = sqlite3.connect(ConfReader.GetSyncDBPath())

    db.row_factory = sqliteUtilities.dict_factory

    c = db.cursor()

    if platformID is None:
        c.execute("select a.*,ad.BuildPath,ad.Size from apps as a inner join appdetails as ad on a.Id  = ad.AppID where ad.PlatformId=1 and ModifiedDate > '" + (lastSyncDateTime) + "';")
    else:
        c.execute("select a.*,ad.BuildPath,ad.Size from apps as a inner join appdetails as ad on a.Id  = ad.AppID where ad.PlatformId="+str(platformID)+" and ModifiedDate > '" + (lastSyncDateTime) + "';")

    results = c.fetchall()


    for result in results:
        strQuery = "select * from AppsBoxMapping where ReferenceID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['BoxMappings'] = results2

    response['ReturnObject'] = results


    print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
        response = {'result': str(e)}



#print json.JSONEncoder().encode(response)

