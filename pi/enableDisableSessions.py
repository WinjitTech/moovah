import urllib2,json
import sqlite3
import sys, getopt
import os


connectedIPs = os.system("netstat -n | grep :3128 | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq")

for ip in connectedIPs:
    if ip is not 0:
        print ip
    else:
        print '0.0.0.0'