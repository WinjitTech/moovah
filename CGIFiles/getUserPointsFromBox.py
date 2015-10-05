#!/usr/bin/python

import cgi
import json
import sqlite3

form = cgi.FieldStorage()

UserID = form.getvalue('userid')

print "Content-type: application/json\n\n"

response =""        
    
try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()     
    
    c.execute("select PointsBalance from Users where userID = " + str(UserID) + ";")
    
    pointsFromBox = c.fetchone()[0]
    response = {'Points':pointsFromBox}
 
except Exception, e:    
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")        
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)