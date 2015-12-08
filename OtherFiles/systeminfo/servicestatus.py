#!/usr/bin/python

import commands

try:    

    apache2Status = commands.getoutput("service apache2 status")
    squid3Status = commands.getoutput("service squid3 status")

    print "Apache2 status : "+str(apache2Status) +"<br>"
    print "Squid3 status : "+str(apache2Status) +"<br>"


except Exception, e:    
    print "Error in Commands :"+str(e)



