#!/usr/bin/python

import cgi
import json
import sqlite3
import time

form = cgi.FieldStorage()

UserID = (form.getvalue('userid'))
IsAllowed = (form.getvalue('allow'))
Duration = (form.getvalue('duration'))

UserID = str(UserID).strip("'")
IsAllowed = str(IsAllowed).strip("'")
Duration = str(Duration).strip("'")

response =""

print "Content-type: application/json\n\n"

try:
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")

    c = db.cursor()

    # if Timestamp<int(time.time()):

    if (UserID==None) or (UserID == '') or (UserID=='None'):

        response = {'Result':"Invalid userid !!"}

    else:

        if (Duration==None) or (Duration=='') or (Duration == 'None'):
            Duration=2

        # Set timestamp = Current time + 2 minutes to allow internet to users
        Timestamp = int(time.time())+(int(Duration)*60)

        if IsAllowed.capitalize()=="True":
            cmd = "UPDATE Users SET DataBalance="+str(Timestamp)+" WHERE userID = '"+UserID+"';"
            c.execute(cmd)
            response = {'Result':True,'CTime':time.ctime(time.time()),'Timestamp':time.ctime(Timestamp)}
        else:
            cmd = "UPDATE Users SET DataBalance="+str(int(time.time()))+" WHERE userID = '"+UserID+"';"
            c.execute(cmd)
            response = {'Result':False,'CTime':time.ctime(time.time()),'Timestamp':time.ctime(int(time.time()))}
    db.commit()
    db.close()

except Exception, e:
    response = {'Result': str(e)}



print json.JSONEncoder().encode(response)



