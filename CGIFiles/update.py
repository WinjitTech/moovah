import sqlite3
import os
import MoovahLogger


def UpdateDB():

    try:

        sudoPassword = 'winjit123'
        result=""
        command = "python /home/pi/SyncDB/SyncBox.py"

        result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        MoovahLogger.logger.debug("Command Executed :"+str(command))

    except Exception,e:
        MoovahLogger.logger.error(str(e))

UpdateDB()