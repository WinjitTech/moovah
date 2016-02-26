#!/usr/bin/python

import json
import os
import MoovahLogger


response =""

try:
    sudoPassword = 'winjit123'
    result=""
    command = "python /home/pi/SyncDB/SyncBox.py"

    result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    MoovahLogger.logger.debug("Command Executed :"+str(command))

except Exception,e:
        MoovahLogger.logger.error("RunCommand: "+str(e))
