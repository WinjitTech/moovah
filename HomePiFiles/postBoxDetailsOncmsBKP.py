import urllib2,json
import sqlite3
import sys, getopt
import os
import commands
import platform

a = commands.getoutput("df -h /dev/root")
SDCARD = a[49:58]
SizeOfSDCard = a[65:69]
UsedOfSDCard = a[71:75]
FreeSpaceOnSDCard = a[77:81]
PercentUsedOfSDCard = a[83:86]
MountedPathOfSDCard = a[87]
SDCardCompany = "SonySDCard"

print "SDCardCompany: "+SDCardCompany
print "SDCARD: "+SDCARD
print "SizeOfSDCard: "+SizeOfSDCard
print "UsedOfSDCard: "+UsedOfSDCard
print "FreeSpaceOnSDCard: "+FreeSpaceOnSDCard
print "PercentUsedOfSDCard: "+PercentUsedOfSDCard
print "MountedPathOfSDCard: "+MountedPathOfSDCard

b = commands.getoutput("df -h /dev/sda1")
PenDrive = b[49:58]
SizeOfPenDrive = b[66:69]
UsedOfPenDrive = b[71:75]
FreeSpaceOnPenDrive = b[78:81]
PercenteUsedOfPenDrive = b[83:86]
MountedPathOfPenDrive = b[87:]

print "PenDrive: "+PenDrive
print "SizeOfPenDrive: "+SizeOfPenDrive
print "UsedOfPenDrive: "+UsedOfPenDrive
print "FreeSpaceOnPenDrive: "+FreeSpaceOnPenDrive
print "PercenteUsedOfPenDrive: "+PercenteUsedOfPenDrive
print "MountedPathOfPenDrive: "+MountedPathOfPenDrive

file = open("/proc/cpuinfo",'r')
row = file.readlines()
ModelName1 = row[1]
Hardware1 = row[9]
Revision1 = row[10]
Serial1 = row[11]

ModelName = ModelName1[13:]
Hardware = Hardware1[11:]
Revision = Revision1[11:]
Serial = Serial1[10:]
KernelVersion = platform.platform()

print "ModelName: "+ModelName
print "Hardware: "+Hardware
print "Revision: "+Revision
print "Serial: "+Serial
print KernelVersion

#c = commands.getoutput("lsusb | tail -2")
#NameOfPenDrive = c[115:]
#NameOfWifiAdapter = c[33:60]

#print "NameOfPenDrive: "+NameOfPenDrive
#print "NameOfWifiAdapter: "+NameOfWifiAdapter

#############Pendrive########################
NameOfPenDrive = commands.getoutput("cat /sys/block/sda/device/vendor")
print "NameOfPenDrive: "+NameOfPenDrive
NameOfWifiAdapter = 'NA'
print "NameOfWifiAdapter: "+NameOfWifiAdapter

os_name = open("/etc/os-release",'r')
ans = os_name.readlines()
NameOfOS1 = ans[0]
Version1 = ans[3]

NameOfOS = NameOfOS1[12:]
Version = Version1[9:19]

print "NameOfOS: "+NameOfOS
print "Version: "+Version


SimNumber = 'No Sim'


try:
        
    db = sqlite3.connect("/home/pi/pythonlogger.py/data.db")
    c = db.cursor()

    #records = c.execute("SELECT BoxID FROM Box LIMIT 1;");

    BoxID = None
    Name="Dummy"

    for record in c.fetchall():
        BoxID = record[0]

    if BoxID is None or BoxID is "":
        BoxID = None
    MacID = open('/sys/class/net/eth0/address').read()
    print MacID	
    #MacID = "TestMacIDLocal" #os.("/sbin/ifconfig eth0 |awk '/HWaddr/{print $5}'").read()
    url=''
    
    if BoxID is None:
        print 'Create Box'
        url = 'http://moovahapp.com/Live/LiveAPI/CreateAndMapBox'
        postdata = {'Name':str(Name),'SIMNumber':str(SimNumber),'MacAddress':str(MacID),
                    'RPIOS':str(NameOfOS),'RPIOSVersion':str(Version),'RPIKernelVersion':str(KernelVersion),
                    'RPIModelName':str(ModelName),'RPIHardware':str(Hardware),'RPIRevision':str(Revision),
                    'RPISerialNo':str(Serial),'WifiAdapterCompany':str(NameOfWifiAdapter),'SDCardMountedPath':str(MountedPathOfSDCard),
                    'SDCardCompany':str(SDCardCompany),'SDCardSize':str(SizeOfSDCard),'SDCardUsed':str(UsedOfSDCard),
     		     'PenDriveCompany':str(NameOfPenDrive),
                    'PenDriveMountedPath':str(MountedPathOfPenDrive),'PenDriveSize':str(SizeOfPenDrive),'PenDriveUsed':str(UsedOfPenDrive)
    	            }
    	print "create"
    	#print postdata
    else:
    	print 'update Box'
	url = 'http://moovahapp.com/Live/LiveAPI/UpdateBox'
	postdata = {'BoxID':BoxID,'MacAddress':str(MacID),'SIMNumber':str(SimNumber),'RPIOS':str(NameOfOS),
                    'RPIOSVersion':str(Version),'RPIKernelVersion':str(KernelVersion),
                    'RPIModelName':str(ModelName),'RPIHardware':str(Hardware),'RPIRevision':str(Revision),
		    'RPISerialNo':str(Serial),'WifiAdapterCompany':str(NameOfWifiAdapter),'SDCardMountedPath':str(MountedPathOfSDCard),
                    'SDCardCompany':str(SDCardCompany),'SDCardSize':str(SizeOfSDCard),'SDCardUsed':str(UsedOfSDCard),
		    'PenDriveCompany':str(NameOfPenDrive),'PenDriveMountedPath':str(MountedPathOfPenDrive),'PenDriveSize':str(SizeOfPenDrive),
		    'PenDriveUsed':str(UsedOfPenDrive)
        	   }
	print "update"
	#print postdata
   
    req = urllib2.Request(url)
    req.add_header('Content-Type','application/json')
    data = json.dumps(postdata)
    print data	
    response = urllib2.urlopen(req,data)

    data = json.loads(response.read())
    BoxID =  data["ReturnObject"][0]["BoxID"]
    c.execute("delete from Box;")
    c.execute("insert or replace into Box(BoxID,MacID,IsActive) values(?,?,?);",(BoxID,MacID,1))

    db.commit()

    print "BoxID is " + str(BoxID)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("boxdetails.py"+"######"+str(e)+"\r\n")
        print str(e)