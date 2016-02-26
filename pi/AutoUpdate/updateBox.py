__author__ = 'pi'

import os
import shutil
import time

import Schedular


def copyFile(src,dst):
    shutil.copy(src,dst)

def copyAllFilesToDir(src,dst):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dst)

def runCommand(command,isSudo):
    #os.system("sudo iptables -I FORWARD -p tcp -m multiport ! --dport 21,22,23,80 -j DROP")
    sudoPassword = 'winjit123'
    #command = 'sudo iptables -I FORWARD -p tcp -m multiport ! --dport 21,22,23,80 -j DROP '
    result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    return result

def runCommandsOnBox(commands):
    for cmd in commands:
        print runCommand(cmd)


def StartDef():
    #copyFile("/home/pi/srcfdr/squid.conf","/home/pi/dstfdr/")
    copyAllFilesToDir("/home/pi/srcfdr","/home/pi/dstfdr/")

def TestFunc():
    print "Test Func() is called:"
    return True

if __name__ == "__main__":
    #StartDef()
    commands=[]
    commands=[
        "sudo iptables -I FORWARD -p tcp -m multiport ! --dport 21,22,23,80 -j DROP",
        "sudo iptables -I FORWARD -p tcp -m multiport ! --dport 21,22,23,80 -j DROP"
    ]

    Schedular.TRunAtEvery(-1,-1,-1,-1,-1,10,TestFunc)
    time.sleep(40)
    Schedular.KillAllThreads()
    #runCommandsOnBox(commands)

