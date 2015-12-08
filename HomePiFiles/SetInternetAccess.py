#!/usr/bin/python

import sqlite3
import time

try:
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")

    c = db.cursor()

    CTimeStamp = int(time.time())

    strQuery = "SELECT IP,DataBalance FROM Users;"
    c.execute(strQuery);

    fd = open("/etc/squid3/whitelist", 'r')
    whitelist = fd.readlines()
    whitelist = [x.replace("\r\n", " ") for x in whitelist]
    fd.close()
    print whitelist

    with open("/etc/squid3/whitelist", "w+") as myfile:
        for record in c.fetchall():
            IP = record[0]
            Timestamp = record[1]

            if (int(Timestamp) < int(CTimeStamp)) and (int(Timestamp) > 0):
                print whitelist
                print "IP: " + str(IP)
                if IP in whitelist:
                    whitelist.remove(IP)
                if str(IP) + " " in whitelist:
                    whitelist.remove(str(IP) + " ")
                print "Internet blocked for : " + str(IP)
            else:
                print "Internet allowed for : " + str(IP)
        print whitelist
        whitelist = [x.replace(" ", "\r\n") for x in whitelist]
        myfile.writelines(whitelist)
    db.close()

except Exception, e:
    print "Error : " + str(e)
