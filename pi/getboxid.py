#!/usr/bin/python

import cgi, cgitb
import json
import sqlite3

form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"

try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()     
    
    c.execute("select BoxID from Box where IsActive=1;")
    
    BoxID = c.fetchone()[0]
    response = {'boxid':BoxID}
    
except Exception, e:    
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")        
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)


