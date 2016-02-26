import sqlite3
import GetCMSData
import FileMgr
import ConfReader
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


                if 'Id' in key:
                    print('Record Added/Updated for '+tblName+' :'+str(value))

                if 'AlbumDetails' in key:
                    insertOrUpdateRecord(value,'AlbumDetails')
                else:
                    if 'BoxMappings' in key:
                        insertOrUpdateRecord(value,"ArticleBoxMapping")
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

imgpath = GetCMSData.GetData('SubCategories')

insertOrUpdateRecord(imgpath,"SubCategory")

MoovahLogger.logger.info("SubCategories updated successfully")