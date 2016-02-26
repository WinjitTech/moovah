#!/usr/bin/python

import cgi
import json
import commands

form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"
try:
    b = commands.getoutput("df -h /dev/sda1")

    PenDrive = b[49:58]
    SizeOfPenDrive = b[66:69]
    UsedOfPenDrive = b[71:75]
    FreeSpaceOnPenDrive = b[78:81]
    PercenteUsedOfPenDrive = b[83:86]
    MountedPathOfPenDrive = b[87:]

    response={'PenDrive': PenDrive,
                'SizeOfPenDrive': SizeOfPenDrive,
                'UsedOfPenDrive': UsedOfPenDrive,
                'FreeSpaceOnPenDrive': FreeSpaceOnPenDrive,
                'PercenteUsedOfPenDrive':PercenteUsedOfPenDrive}
except Exception, e:
    print str(e)
    response={'Error':str(e)}
print json.JSONEncoder().encode(response)
