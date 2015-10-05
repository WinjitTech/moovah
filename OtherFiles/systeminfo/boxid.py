#!/usr/bin/python

import sqlite3

try:    
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     

    c = db.cursor()     
    
    c.execute("select BoxID from Box where IsActive=1;")

    BoxID = "-1"

    for record in c.fetchall():
        BoxID = record[0]

    print "Your Box ID is : "+str(BoxID) +"<br>"

    MacID = open('/sys/class/net/eth0/address').read()
    print "Your Mac ID is : "+str(MacID)

except Exception, e:    
    print "Error in Box :"+str(e)



