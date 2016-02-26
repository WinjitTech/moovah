#!/usr/bin/python

import cgi
import json
import sqlite3

import sqliteUtilities
import ConfReader

form = cgi.FieldStorage()

#lastSyncDateTime= "0001-01-01 00:00:00.000" #datetime.datetime.now()

lastSyncDateTime = (form.getvalue('lastSyncDateTime'))

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""

#response['Date']=lastSyncDateTime

print "Content-type: application/json\n\n"


try:

    db = sqlite3.connect(ConfReader.GetSyncDBPath())

    db.row_factory = sqliteUtilities.dict_factory

    c = db.cursor()

    strquery = "select * from Album where ModifiedDate > '" + (lastSyncDateTime) + "';"

    c.execute(strquery)


    results = c.fetchall()

    for result in results:
        strQuery = "select * from albumdetails where AlbumID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['AlbumDetails'] = results2


    for result in results:
        strQuery = "select * from albumboxmapping where ReferenceID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['BoxMappings'] = results2

    response['ReturnObject'] = results


    print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")


#print json.JSONEncoder().encode(response)

