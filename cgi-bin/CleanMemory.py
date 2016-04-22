#!/usr/bin/python

import cgi
import json
import commands
form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"

try:
    a = commands.getoutput("sudo cat /dev/null > /var/log/auth.log")
    print a

except Exception, e:
    print str(e)
