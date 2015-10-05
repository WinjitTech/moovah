import sqlite3
0

def updateWhitelist():

    try:
        db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
        c = db.cursor()

        with open("/etc/squid3/whitelist", "w") as myfile:

            myfile.write("192.168.5.1"+"\r\n")

            c.execute("SELECT DISTINCT IP,DataBalance FROM Users ;");
            for record in c.fetchall():
                IP = record[0]
                DataBalance = record[1]

                if DataBalance > 0:
                    myfile.write(str(IP)+"\r\n")

        print "users updated to whitelist"

    except Exception,e:
        print str(e)
    
updateWhitelist()