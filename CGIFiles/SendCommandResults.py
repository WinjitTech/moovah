#!/usr/bin/python

import cgi
import json

form = cgi.FieldStorage()

CommandKey = str(form.getvalue('CommandKey'))
CommandStatus = str(form.getvalue('CommandStatus'))

response =""

print "Content-type: application/json\n\n"

try:
    #db = sqlite3.connect("/home/pi/RemotePIControl/data.db")
    #db = sqlite3.connect("D:\\shri\\data.db")
    # c = db.cursor()
    #
    # c.execute("select BoxID from Box where IsActive=1;")
    #
    # BoxID = "-1"
    #
    # for record in c.fetchall():
    #     BoxID = record[0]

    response = {'Success':'True'}

except Exception, e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)


