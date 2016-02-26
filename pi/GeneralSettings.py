import sqlite3

import GetCMSData
import FileMgr
import ConfReader

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


                #Check if it is a file to download and download it.
                if "IsActive" in jsondata[i].keys():
                    if jsondata[i]["IsActive"]==1:
                        FileMgr.CheckAndDownloadFile(key,value)
                else:
                    FileMgr.CheckAndDownloadFile(key,value)


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
    db.commit()



# lastSyncDateTime= "0001-01-01%2000:00:00.000" #datetime.datetime.now()
#
# apiurl = "http://168.63.241.212/API/GetGeneralSettings/"+str(lastSyncDateTime)
# j = urllib2.urlopen(apiurl)
# js = json.load(j)
# imgpath = js['ReturnObject']
# results = len(imgpath)

db = sqlite3.connect(ConfReader.GetSyncDBPath())
c = db.cursor()

imgpath = GetCMSData.GetData('GeneralSettings')

insertOrUpdateRecord(imgpath,"GeneralSetting")
