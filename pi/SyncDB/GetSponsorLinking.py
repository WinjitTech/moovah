import sqlite3
import ConfReader
import FileMgr
import GetCMSData
import MoovahLogger
import SyncDBMgr as c

def insertOrUpdateRecord(jsondata,tblName):


    for i in range(len(jsondata)):
        Id = jsondata[i]['Id']

        query ="delete from "+tblName+" where Id='"+str(Id)+"'"

        c.execute(query)

        query ='insert into '+tblName+'('
        cols = ''
        vals = ''
        try:
            for key in jsondata[i].keys():

                try:
                    key = key.encode('UTF-8')
                except Exception,e:
                    key = key

                value =jsondata[i][key]

                try:
                    value = value.encode('UTF-8')
                except Exception,e:
                    value = value

                try:
                    value = value.replace('"','')
                except Exception,e:
                    value = value

                if value is not None:
                    cols = cols + key + ','
                    vals = vals +'"'+ str(value)+ '",'

            query += cols[:-1] +') values('+vals[:-1]+');'
            c.execute(query)

            if 'Id' in key:
                print('Record Added/Updated for '+tblName+' :'+str(value))

        except Exception,e:
            print 'Insert Error for ['+ tblName +'] id=' + str(Id) +' details:'+ str(e)
            continue



query ="CREATE TABLE IF NOT EXISTS 'SponsorLinking' "+ "('Id' INTEGER PRIMARY KEY NOT NULL, 'ModuleId' INTEGER, 'ReferenceId' INTEGER, 'SponsorType' INTEGER, " + "'Type' TEXT, 'ModifiedDate' TEXT)";
c.execute(query)

imgpath = GetCMSData.GetData('SponsorLinking')

insertOrUpdateRecord(imgpath,"SponsorLinking")

MoovahLogger.logger.info("SponsorLinking updated successfully")