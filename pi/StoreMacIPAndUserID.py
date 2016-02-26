#!/usr/bin/python

import cgi, cgitb
import json
import sqlite3

form = cgi.FieldStorage()

macid = str(form.getvalue('macid'))
ip = str(form.getvalue('ip'))
userid = str(form.getvalue('userid'))

response =""

print "Content-type: application/json\n\n"

try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()     
    
    c.execute("select Count(*) from Users where MacID = " + str(macid) + ";")    
    
    
    recordCount = c.fetchone()[0]
    
    if recordCount>0:
        if userid is None:
            c.execute("UPDATE Users SET MacID=?,  IP=?, userID=? WHERE MacID = ?;",(macid,ip,userid,macid))
        else:        
            c.execute("UPDATE Users SET MacID=?,  IP=?, userID=?,IsConnected=1 WHERE MacID = ?;",(macid,ip,userid,macid))
    else:    
        if userid is None:
            c.execute("insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected) values(?,?,?,?,?,?,?,?);",(ip,macid,0,0,0,0,userid,0))
        else:
            c.execute("insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected) values(?,?,?,?,?,?,?,?);",(ip,macid,0,0,1,0,userid,1))

    
    db.commit()    
    response = {'result':'true','macID':macid,'IP':ip,'UserID':userid}
    
except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")        
        response = {'result': str(e)}



print json.JSONEncoder().encode(response)


