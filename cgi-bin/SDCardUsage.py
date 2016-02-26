#!/usr/bin/python

import cgi
import json
import commands
form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"

try:
    a = commands.getoutput("df -h /dev/root")
    SDCARD = a[49:58]
    SizeOfSDCard = a[65:69]
    UsedOfSDCard = a[71:75]
    FreeSpaceOnSDCard = a[77:81]
    PercentUsedOfSDCard = a[83:86]
    MountedPathOfSDCard = ""
    SDCardCompany = "SonySDCard"

    response = {'SDCardSize':SizeOfSDCard,
                'UsedOfSDCard': UsedOfSDCard,
                'FreeSpaceOnSDCard':FreeSpaceOnSDCard,
                'PercentUsedOfSDCard' :PercentUsedOfSDCard}

except Exception, e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")
    response = {'error': str(e)}

print json.JSONEncoder().encode(response)
