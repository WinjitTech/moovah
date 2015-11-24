#!/usr/bin/python

import cgi
import json
import sqlite3

form = cgi.FieldStorage()

macid = form.getfirst("macid")
ip = form.getfirst("ip")
userid = form.getfirst("userid")


macid = str(macid).strip("'")
ip = str(ip).strip("'")
userid = str(userid).strip("'")

response =""

print "Content-type: application/json\n\n"

try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()     

    if userid is None:
            c.execute("select Count(*) from Users where IP = '" + str(ip) + "' or MacID = '" + str(macid) + "';")
    else:
            c.execute("select Count(*) from Users where IP = '" + str(ip) + "' or userID = '" + str(userid) + "' or MacID = '" + str(macid) + "';")

    recordCount = 0
    for record in c.fetchall():
        recordCount = record[0]


    if recordCount > 1:
        c.execute("delete from Users where IP = '" + str(ip) + "' or userID = '" + str(userid) + "' or MacID = '" + str(macid) + "';")

    isCreated=False
    strQuery=""

    if recordCount>0:

        isCreated=False

        if userid is None:
            c.execute("UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', userID='"+str(userid)+"',IsConnected=0 WHERE IP ='"+str(ip)+"';")
        else:        
            c.execute("UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', userID='"+str(userid)+"',IsConnected=0 WHERE IP = '" + str(ip) + "' or userID = '" + str(userid) + "' or MacID = '" + str(macid) + "';")
    else:

        isCreated=True

        if userid is None:
            c.execute("insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected) values(?,?,?,?,?,?,?,?);",(str(ip),macid,0,0,0,0,userid,0))
        else:
            c.execute("insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected) values(?,?,?,?,?,?,?,?);",(str(ip),macid,0,0,1,0,userid,1))

    
    db.commit()
    db.close()
    response = {'result':'true','macID':macid,'IP':ip,'UserID':userid,'recordCount':recordCount,'IsCreated':isCreated}
    
except Exception,e:
	with open("PythonErrors.txt", "a") as myfile:
		myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")        
	response = {'result': str(e)}



print json.JSONEncoder().encode(response)


