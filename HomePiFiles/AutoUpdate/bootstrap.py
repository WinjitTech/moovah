import sqlite3
import Schedular
import MoovahLogger


def StartSystem():

    try:

        db = sqlite3.connect("/home/pi/AutoUpdate/Autoupdate.sqlite")
        c = db.cursor()

        #Step 1: Schedule existing tasks from schedule database.


        #Step 2: Get Remote API Paths from database.
        Schedular.runCommand("python /home/pi/AutoUpdate/upgrade.py",1)

    except Exception,e:
        MoovahLogger.logger.error(str(e))
    finally:
        db.close()

StartSystem()