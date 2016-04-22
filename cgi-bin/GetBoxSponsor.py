#!/usr/bin/python

import cgi
import json
import sqlite3

form = cgi.FieldStorage()

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""

print "Content-type: application/json\n\n"

try:
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
    # db = sqlite3.connect("D:\\shri\\data.db")
    c = db.cursor()
    c.execute("select * from generalSettings")
    results = []
    for record in c.fetchall():
        result={}
        result["Id"] = record[0]
        result["Name"]= record[1]
        result["Instructions"]= record[2]
        result["SponsorURL"]= record[3]
        result["SponsorImage"]= record[4]
        if record[6]=="True":
            result["IsEarnMoreSponsor"]=bool("true")
        else:
            result["IsEarnMoreSponsor"]= bool("")
        results.append(result)

    response['ReturnObject']=results
    db.close()
except Exception, e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py " + "###### " + str(e) + "\n")
    response = {'error': str(e)}
    print str(e)


print json.JSONEncoder().encode(response)



