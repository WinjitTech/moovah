#!/usr/bin/python

import cgi
import json
import sqlite3
import ConfReader
import urllib2
form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"

try:
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
    c = db.cursor()
    c.execute("select BoxVersion from upgradeSettings;")

    BoxVersion = "-1"

    for record in c.fetchall():
        BoxVersion = record[0]

    db.close()

    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
    c = db.cursor()
    c.execute("select BoxID from Box where IsActive=1;")

    BoxID = "-1"

    for record in c.fetchall():
        BoxID = record[0]

    apiurl =ConfReader.GetAPIURLCom() +"GetBoxVersionNew/"+ str(BoxID)
    #print apiurl
    j = urllib2.urlopen(apiurl)
    js = json.load(j)
    GlobalVersion = js['ReturnObject'][0]['GlobalVersion']

    if BoxVersion>=GlobalVersion:
        upgradeflag=0
    else:
        upgradeflag=1

    response = {'boxversion':BoxVersion,
                'globalversion':GlobalVersion,
                'upgradeflag': upgradeflag}

except Exception, e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)


