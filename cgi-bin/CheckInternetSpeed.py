#!/usr/bin/python

import cgi
import json
import commands

response =""

print "Content-type: application/json\n\n"


try:
    b = commands.getoutput("wget -O speedtest-cli https://raw.github.com/sivel/speedtest-cli/master/speedtest_cli.py")
    a=b[893:904]
    a=a.replace('(','')
    a=a.replace(')','')
    #print a
    response={"Internet Speed": a}
except Exception, e:
    #print(str(e))
    response={"Error": str(e)}

print json.JSONEncoder().encode(response)


