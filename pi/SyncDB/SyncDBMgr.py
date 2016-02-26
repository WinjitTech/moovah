import sqlite3
import ConfReader
import time
import MoovahLogger

def execute(strQuery):

    try:
        NoOfAttempts=10

        con = sqlite3.connect(ConfReader.GetSyncDBPath())
        con.isolation_level=None
        c = con.cursor()

        while NoOfAttempts>0:

            NoOfAttempts-=1
            try:
                c.execute(strQuery)
                con.commit()
                break

            except Exception,e:
                print("Insert error (Retry atempt:"+str(NoOfAttempts))
                time.sleep(5)
                continue

    except Exception,e:
        print str(e)
        MoovahLogger.logger.info("[SyncDB] error in query : "+str(e))

    finally:
        if con:
            con.close()