import sqlite3


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
                    #os.system("sudo iptables -t nat -D PREROUTING -i wlan0 -s "+ str(IP) +" -p tcp --dport 443 -DNAT --to 192.168.5.51:3128")
                    #This iptables command removes the entry from nat table if already present

        print "users updated to whitelist"

    except Exception,e:
        print str(e)
    
updateWhitelist()