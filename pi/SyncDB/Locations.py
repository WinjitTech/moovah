import sqlite3
import MoovahLogger
import GetCMSData
import ConfReader
import SyncDBMgr as c

def insertOrUpdateRecord(jsondata,tblName):


    for i in range(len(jsondata)):
        Id = jsondata[i]['Id']

        query ="delete from "+tblName+" where Id='"+str(Id)+"'"

        c.execute(query)

        if "BoxID" in jsondata[i].keys() and "ReferenceID" in jsondata[i].keys():
            query ="delete from "+tblName+" where BoxID='"+str(jsondata[i]['BoxID'])+"'" + " and ReferenceID='"+str(jsondata[i]['ReferenceID'])+"'"
            print('Record deleted for '+tblName+' :'+str(Id))
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

                if 'Id' in key:
                    print('Record Added/Updated for '+tblName+' :'+str(value))

                if value is not None:
                    cols = cols + key + ','
                    vals = vals +'"'+ str(value)+ '",'

            query += cols[:-1] +') values('+vals[:-1]+');'
            c.execute(query)
            #print(query)

        except Exception,e:
            print 'Insert Error for ['+ tblName +'] id=' + str(Id) +' details:'+ str(e)
            continue

imgpath = GetCMSData.GetData('Locations')

insertOrUpdateRecord(imgpath,"Locations")

MoovahLogger.logger.info("Locations updated successfully")