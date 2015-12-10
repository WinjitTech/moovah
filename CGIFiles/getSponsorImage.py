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
    results=[]
    result={}

    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")     
    #db = sqlite3.connect("D:\\shri\\data.db")     
    c = db.cursor()

    c.execute("select value from generalSettings where key='SponsorURL';")

    SponsorURL = ""
    for record in c.fetchall():
        SponsorURL = record[0]

    result['SponsorURL'] = SponsorURL

    c.execute("select value from generalSettings where key='SponsorImage';")

    SponsorImage = ""
    for record in c.fetchall():
        SponsorImage = record[0]

    result['SponsorImage'] = SponsorImage

    results.append(result)

    response['ReturnObject'] = results
    
except Exception, e:    
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")        
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)


