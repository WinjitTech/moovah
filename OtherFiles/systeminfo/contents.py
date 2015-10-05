import commands

a = commands.getoutput("df -h /dev/root")
SDCARD = a[49:58]
SizeOfSDCard = a[65:69]
UsedOfSDCard = a[71:75]
FreeSpaceOnSDCard = a[77:81]
PercentUsedOfSDCard = a[83:86]
MountedPathOfSDCard = a[87]

#print "SD Card Company: "+SDCardCompany+ "#"
print "SD Card mount location: "+SDCARD+ "#"
print "Size of SD Card: "+SizeOfSDCard+ "#"
print "Memory used on SD Card: "+UsedOfSDCard+ "#"
print "Free space available on SD Card: "+FreeSpaceOnSDCard+ "#"
print "Percent memory used on SD Card: "+PercentUsedOfSDCard+ "#"
print "Mounted path of SD Card: "+MountedPathOfSDCard+ "#"
print "<br><br>"
b = commands.getoutput("df -h /dev/sda1")
PenDrive = b[49:58]
SizeOfPenDrive = b[66:69]
UsedOfPenDrive = b[71:75]
FreeSpaceOnPenDrive = b[78:81]
PercenteUsedOfPenDrive = b[83:86]
MountedPathOfPenDrive = b[87:]

print "Pen Drive mount location: "+PenDrive+ "#"
print "Size of Pen Drive: "+SizeOfPenDrive+ "#"
print "Memory used on Pen Drive: "+UsedOfPenDrive+ "#"
print "Free space available on Pen Drive: "+FreeSpaceOnPenDrive+ "#"
print "Percent memory used on Pen Drive: "+PercenteUsedOfPenDrive+ "#"
print "Mounted path of Pen Drive: "+MountedPathOfPenDrive+ "#"
