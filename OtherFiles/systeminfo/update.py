#!/usr/bin/python

import sqlite3

try:
    db = sqlite3.connect("/home/pi/AutoUpdate/Schedular.sqlite")
    c = db.cursor()

    c.execute("select * from schedule;")
    for row in c.fetchall():
        fileName = row[1]
        NextExeTime = row[2]
        Interval = row[5]
        print 'Name of Schedule: '+str(fileName)+'#'
        print 'Next Execution Time: '+str(NextExeTime)+'#'
        print 'Interval (in seconds): '+str(Interval)+'#'

    db.close()

    print 'Result'+'update has been scheduled for run, please do not disconct box while update is in progress'

except Exception, e:
    print 'Error: '+str(e)
