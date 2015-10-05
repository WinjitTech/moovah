
os_name = open("/etc/os-release",'r')
ans = os_name.readlines()
NameOfOS1 = ans[0]
Version1 = ans[3]

NameOfOS = NameOfOS1[12:]
Version = Version1[9:19]

print "Name of OS : "+NameOfOS +"#"
print "Version : "+Version + "#"
