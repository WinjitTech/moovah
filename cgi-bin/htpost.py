#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>User id and Credit balance</title></head>

<body>

  <h3>User id and Credit balance </h3>
"""

form = cgi.FieldStorage()
#message = form.getvalue("message", "(no message)")
userid = form.getvalue("userid")
balance = form.getvalue("balance")

print """

<!--  <p>Previous message: %s</p> -->

  <p>form

  <form method="post">
    <p>userid: <input type="text" name="userid"/></p>
<!--    <p>balance: <input type="text" name="balance"/></p> -->
  </form>

</body>

</html>
"""%userid
