#!/usr/bin/python

import cgi
import json
import sqlite3

import sqliteUtilities
import ConfReader

form = cgi.FieldStorage()

platformID = (form.getvalue('platformID'))

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""


print "Content-type: application/json\n"


try:
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    db = sqlite3.connect("/home/pi/AutoUpdate/Schedular.sqlite")

    db.row_factory = sqliteUtilities.dict_factory

    c = db.cursor()

    if (platformID is None) or (platformID is '') or (platformID=='1'):
        c.execute("select AndroidVersion from generalSettings;")
        for result in c.fetchall():
            Version = result['AndroidVersion']
            break
    else:
        c.execute("select BlackBerryVersion from generalSettings;")
        for result in c.fetchall():
            Version = result['BlackBerryVersion']
            break


    print Version

except Exception,e:
    print(str(e))

