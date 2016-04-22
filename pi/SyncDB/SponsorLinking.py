import sqlite3
import ConfReader
import FileMgr
import GetCMSData
import MoovahLogger
import SyncDBMgr as c
import json


def insertOrUpdateRecord(jsondata, tblName, ModuleId):
    for i in range(len(jsondata)):
        Id = jsondata[i]['Id']

        query = "delete from " + tblName + " where Id='" + str(Id) + "'"

        c.execute(query)
        #	print query
        query = 'insert into ' + tblName + '('
        cols = ''
        vals = ''
        try:
            for key in jsondata[i].keys():

                try:
                    key = key.encode('UTF-8')
                except Exception, e:
                    key = key

                value = jsondata[i][key]

                try:
                    value = value.encode('UTF-8')
                except Exception, e:
                    value = value

                try:
                    value = value.replace('"', '')
                except Exception, e:
                    value = value

                if value is not None:
                    cols = cols + key + ','
                    vals = vals + '"' + str(value) + '",'
                #	    print vals
            query += cols[:-1] + ') values(' + vals[:-1] + ');'
            c.execute(query)

            if 'Id' in key:
                print('Record Added/Updated for ' + tblName + ' :' + str(value))

        except Exception, e:
            print 'Insert Error for [' + tblName + '] id=' + str(Id) + ' details:' + str(e)
            continue

imgpath = GetCMSData.GetData('SponsorLinking')

insertOrUpdateRecord(imgpath, "SponsorLinking", None)

MoovahLogger.logger.info("SponsorLinking updated successfully")
