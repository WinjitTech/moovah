#!/usr/bin/python

import urllib2
import ConfReader
import json

print "Content-type: application/json\n\n"

strConfigPath ="/home/pi/moovah.config"

def internet_on():
    try:
        url = ConfReader.GetAPIURL()
        response=urllib2.urlopen('http://www.google.com',timeout=20)
        return response
    except urllib2.URLError as err: pass
    return False


def main():
    status=internet_on()
    if status:
        response = {'Internet_Response': true}
        print json.JSONEncoder().encode(response)
    else:
        response={'Internet_Response': False}
    print json.JSONEncoder().encode(response)
if __name__ == "__main__":
    main()
