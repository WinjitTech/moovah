#!/usr/bin/python

import sqlite3
import time

try:
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")

    c = db.cursor()

    CTimeStamp = int(time.time())

    strQuery ="SELECT IP,DataBalance FROM Users;"
    c.execute(strQuery);

    fd = open("/etc/squid3/whitelist",'r')
    whitelist = fd.readlines()
    fd.close()

    with open("/etc/squid3/whitelist", "w+") as myfile:
        for record in c.fetchall():
            IP = record[0]
            Timestamp= record[1]

            if (int(Timestamp)<int(CTimeStamp)) and (int(Timestamp)>0):
                print "IP: "+str(IP)
                if IP in whitelist:
                    whitelist.remove(IP)
                # myfile.write(str(IP)+"\r\n")

                print "Internet blocked for : "+str(IP)
            else:
                print "Internet allowed for : "+str(IP)

        myfile.writelines(whitelist)
    db.close()

except Exception, e:
    print "Error : "+str(e)



