import json
import urllib2
import sqlite3
import ConfReader
import getDataUsageByIPs

def readFileToMatrix(fd):
    dataMatrix,i={},0
    while 1:
        l=[]
        data=fd.readline()
        if data =="":
          break
        dd = data.split(" ")
        for item in dd:
          if item != "":
              l.append(item)
        if len(l)==10:
          c,s=l[3].split('/')[0],l[3].split('/')[1]
          ps,ph=l[8].split('/')[0],l[8].split('/')[1]
          l[9]=l[9].strip("\n")
          dataMatrix[i]=[l[0],l[1],l[2],c,s,l[4],l[5],l[6],l[7],ps,ph,l[9]]
          i = i + 1
    return dataMatrix

def readWhitelistFileToArray(fd):
    l=[]
    # while 1:
    # data=fd.readline().replace('\n','')
    # if data =="":
    #   break
    data="moovahapp.com"
    l.append(data)
    data="moovahapp.net"
    l.append(data)
    return l

def main():    

    logFilePath = ConfReader.GetValue(ConfReader.strLogFilePathKey) #'/var/log/squid3/access.log'
    databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'
    WhiteListFilePath = "/home/pi/freeSites"

    fd = open(logFilePath,'r')
    accessLogRecords = fd.readlines()
    fd.close()

    if len(accessLogRecords)==0:
        print "access logs are empty."
        exit()

    fd = open(logFilePath,'r')
    dataMatrix = readFileToMatrix(fd)
    fd.close()
    lFile = open(logFilePath, "w+")
    lFile.close()

    db = sqlite3.connect(databaseFilePath)
    c = db.cursor()

    BoxID = None
    c.execute("SELECT BoxID FROM Box LIMIT 1;");
    for record in c.fetchall():
      BoxID = record[0]

    fd2 = open(WhiteListFilePath,'r')
    whitelistURLArray=readWhitelistFileToArray(fd2)
    fd.close()

    LogData ={}
    UserIDs=''
    i=0
    for key, value in dataMatrix.items():

        BytesUsed = value[5]
        IpAddress = value[2]
        URLVisited = value[7]

        urlvisited = str(URLVisited).replace('http://','')
        urlvisited = str(urlvisited).split('/')
        urlvisited = urlvisited[0]

        # print urlvisited

        isFree=0
        for freeURL in whitelistURLArray:
            freeurl = str(freeURL).replace('http://','')
            freeurl = str(freeurl).split('/')
            freeurl = freeurl[0]

            if freeurl == urlvisited:
                # print "Whitelisted :"+urlvisited +"  ==  ComparedWith: " +freeurl
                isFree=1
                break

        if isFree:
            continue

        # userID=None
        strQuery ="SELECT userID FROM Users where IP='"+str(IpAddress)+"';"
        c.execute(strQuery);
        for record in c.fetchall():
            userID = record[0]

            # if str(userID) not in UserIDs:
            #     UserIDs += str(userID)+','

            LogData[i]={ "UserID":userID ,"Bytes":BytesUsed, "URL":URLVisited,"IpAddress":IpAddress,"BoxID":BoxID }
            i+=1

    # UserIDs =UserIDs[:-1]
    #
    # strQuery ="SELECT userID,IP FROM Users where userID not in ("+UserIDs+");"
    # c.execute(strQuery);
    # for record in c.fetchall():
    #     userID = record[0]
    #     IpAddress = record[1]
    #
    #     if userID is not None:
    #
    #         LogData[i]={ "UserID":userID ,"Bytes":0, "URL":str(ConfReader.GetAPIURL()),"IpAddress":str(IpAddress),"BoxID":BoxID }
    #         i+=1

    #For HTTPS data
    IPList=[]
    strQuery ="SELECT IP FROM Users;"
    c.execute(strQuery);
    for record in c.fetchall():
        IPList.append(record[0])

    # print IPList
    IPHTTPsUsages = getDataUsageByIPs.getDataByIPs(IPList)
    print IPHTTPsUsages

    IPs =""
    for IP in IPHTTPsUsages.keys():
        IPs += "'"+str(IP)+"',"
    IPs =IPs[:-1]
    strQuery ="SELECT userID,IP FROM Users where IP in ("+IPs+");"
    #print strQuery
    c.execute(strQuery);
    for record in c.fetchall():
        userID = record[0]
        IpAddress = record[1]
        BytesUsed = IPHTTPsUsages[IpAddress]
        print("BytesUsed: "+str(BytesUsed))
        if userID is not None:

            LogData[i]={ "UserID":userID ,"Bytes":BytesUsed, "URL":'',"IpAddress":str(IpAddress),"BoxID":BoxID }
            i+=1

    LogSend=0

    try:

        url = ConfReader.GetAPIURLCom() +"BrowsingTransactionNew"

        print url

        postdata = LogData.values()

        print postdata

        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)

        #if DataUsed > 0:
        response = urllib2.urlopen(req,data)
        js = json.load(response)
        #print response
        if js['StatusCode'] == 200:

            LogSend=1

            with open("/etc/squid3/whitelist", "w+") as myfile:
                myfile.write("192.168.5.1"+"\r\n")
                WhiteList = js['ReturnObject'][0]['WhiteList']
                IPList=[]

                for UserID in WhiteList:
                    strQuery ="SELECT IP FROM Users where userID='"+str(UserID)+"';"
                    c.execute(strQuery);
                    for record in c.fetchall():
                        IP = record[0]
                        IPList.append(IP)
                        myfile.write(str(IP)+"\r\n")

            print "RESET:" + str(IPList)
            getDataUsageByIPs.resetDataUsageOfIPs(IPList)
            getDataUsageByIPs.runWhiteList()

        print js

    except Exception, e:
        print str(e)

    finally:

        if LogSend==0:
            lFile = open(logFilePath, "w+")
            lFile.writelines(accessLogRecords)
            lFile.close()
        
if __name__ == "__main__":
    main()           
        
