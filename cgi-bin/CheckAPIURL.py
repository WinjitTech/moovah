#!/usr/bin/python

import urllib2
import cgi
import json

response = ""

print "Content-type: application/json\n\n"


def internet_on():
    try:
        response = urllib2.urlopen('http://www.moovahapp.com',timeout=20)
        return True
    except urllib2.URLError as err : pass
    return False


def main():
    response={"Free_Sites_Response": internet_on()}
    print json.JSONEncoder().encode(response)

if __name__ == "__main__":
    main()     
