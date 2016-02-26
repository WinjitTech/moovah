#!/usr/bin/python

# Import modules for CGI handling 
import cgi
import os
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
#print '<form action="/cgi-bin/posrt.py" method="post">
#First Name: <input type="text" name="userid"><br />
#Last Name: <input type="text" name="balance" />

#<input type="submit" value="Submit" />
#</form> '
# Get data from fields
userid= form.getvalue('userid')
balance= form.getvalue('balance')

#try:
#		db = sqlite3.connect("data.db")
		#print "database opened successfully"
#		cursor = db.cursor()
#		cursor.execute("insert into Dataused(userid,balance) values (?, ?)",(userid,balance))
#		db.commit()
# bandwidth_used(ip varchar(20), bytesused varchar(40))
#		cursor.execute("SELECT * from syncdetails;")
#		cursor.execute("SELECT lastsyncdate from syncdetails order by ROWID DESC limit 1")
#		for row in cursor:
#			sdate = row
#		db.close()
		#print type(sdate)
#except Exception, e:
#		print "databse failed to open "
#		print e

#first_name = form.getvalue('first_name')
#last_name  = form.getvalue('last_name')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>user id and credits of users</title>"
print "</head>"
print "<body>"
print "<h2>credits of user %s are  %s</h2>" % (userid, balance)
print "</body>"

file1 = open("idandcredit.txt","a")
file1.write(str(userid) + "," + str(balance) +"\n")
file1.close()
os.system('./remove.sh')
