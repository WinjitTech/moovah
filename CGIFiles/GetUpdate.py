#!/usr/bin/python

import cgi,sys
import json
import sqlite3
import datetime

form = cgi.FieldStorage()

response ={}

print "Content-type: application/json\n\n"

try:
    db = sqlite3.connect("/home/pi/AutoUpdate/Schedular.sqlite")
    c = db.cursor()

    dtNow = datetime.datetime.now()
    #c.execute("update schedule SET DateTime='"+str(dtNow)+"' where Command like '%update.py%';")
    c.execute("select * from schedule;")
    for row in c.fetchall():
        fileName = row[1]
        NextExeTime = row[2]
        Interval = row[5]
        response[row[0]] = {'Name of Schedule:':str(fileName),'Next Execution Time':NextExeTime,'Interval (in seconds)':Interval}
    db.close()

    #response = {'Result':'update has been scheduled for run, please do not disconct box while update is in progress'}

except Exception, e:
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)
