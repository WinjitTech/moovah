#!/usr/bin/python

import cgi
import json

import ConfReader


form = cgi.FieldStorage()

key = form.getfirst('key')
value = form.getfirst('value')


response =""

print "Content-type: application/json\n\n"

try:
    result = 'true'

    if 'APIURL' in key:
        value = ConfReader.GetAPIURL()
    else:
        if value is None:
            value = ConfReader.GetValue(key)
        else:
            result = ConfReader.UpdateValue(key,value)

    response = {'result':result,key:value}

except Exception, e:
    # with open("PythonErrors.txt", "a") as myfile:
    #     myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")
    response = {'error': str(e)}
    #response = {'error':'error123'}


print json.JSONEncoder().encode(response)

