import sqlite3
import SyncDBMgr as c
import GetCMSData
import FileMgr
import ConfReader
import MoovahLogger

def insertOrUpdateRecord(jsondata,tblName,ParentID):

    if 'AppsBoxMapping' in tblName and ParentID is not None:
        query = "delete from " + tblName + " where ReferenceID='" + str(ParentID) + "'"
        print('Records deleted for ' + tblName + ' for ReferenceID :' + str(ParentID))
        c.execute(query)

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

                #Check if it is a file to download and download it.
                if "IsActive" in jsondata[i].keys():
                    if jsondata[i]["IsActive"]==1:
                        FileMgr.CheckAndDownloadFile(key,value,11,Id)
                else:
                    FileMgr.CheckAndDownloadFile(key,value,11,Id)



                if 'Id' in key:
                    print('Record Added/Updated for '+tblName+' :'+str(value))

                if 'AppDetails' in key:
                    insertOrUpdateRecord(value,'AppDetails',Id)
                else:
                    if 'BoxMappings' in key:
                        insertOrUpdateRecord(value,"AppsBoxMapping",Id)
                    else:
                        if value is not None:
                            cols = cols + key + ','
                            vals = vals +'"'+ str(value)+ '",'

            query += cols[:-1] +') values('+vals[:-1]+');'
            c.execute(query)
            #print(query)

        except Exception,e:
            print 'Insert Error for ['+ tblName +'] id=' + str(Id) +' details:'+ str(e)
            continue


imgpath = GetCMSData.GetData('Apps')

insertOrUpdateRecord(imgpath,"Apps",None)

MoovahLogger.logger.info("Apps updated successfully")