#!/usr/bin/python

import cgi
import json
import sqlite3

form = cgi.FieldStorage()

UserID = str(form.getvalue('userid'))
Transaction = str(form.getvalue('transaction'))
DownloadType = str(form.getvalue('downloadtype'))
CreditPoint = str(form.getvalue('creditpoint'))   
ModuleID = str(form.getvalue('moduleid'))
ReferenceID = str(form.getvalue('referenceid'))
#BoxID = str(form.getvalue('boxid'))


#UserID = str(0)
#Transaction = str(0)
#DownloadType = str(0)
#CreditPoint = str(0)
#ModuleID = str(0)
#ReferenceID = str(0)
#BoxID = str(0)
IsSynced=0

response =""

print "Content-type: application/json\n\n"

try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()     

    c.execute("select BoxID from Box where IsActive=1;")
        
    BoxID = c.fetchone()[0]

    c.execute("SELECT Max(ID) FROM UserTransaction;");

    MaxID = c.fetchone()[0]
    MaxID = MaxID+1

    c.execute("insert into UserTransaction values(?,?,?,?,?,?,?,?,?)",(MaxID,UserID,Transaction,DownloadType,CreditPoint,ModuleID,ReferenceID,BoxID,IsSynced))

    
    db.commit()    
    response = {'result':'true','recordID':MaxID}
    
except Exception, e:
        response = {'result': str(e)}



print json.JSONEncoder().encode(response)


