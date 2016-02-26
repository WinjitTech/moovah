import sqlite3
import ConfReader
import GetCMSData
import FileMgr
import MoovahLogger
import SyncDBMgr as c

def insertOrUpdateRecord(jsondata,tblName,ParentID):

    if 'CompetitionBoxMapping' in tblName and ParentID is not None:
        query = "delete from " + tblName + " where CompetitionID='" + str(ParentID) + "'"
        print('Records deleted for ' + tblName + ' for CompetitionID :' + str(ParentID))
        c.execute(query)

    for i in range(len(jsondata)):
        Id = jsondata[i]['Id']

        query ="delete from "+tblName+" where Id='"+str(Id)+"'"

        c.execute(query)

        if "BoxID" in jsondata[i].keys() and "CompetitionID" in jsondata[i].keys():
            query ="delete from "+tblName+" where BoxID='"+str(jsondata[i]['BoxID'])+"'" + " and CompetitionID='"+str(jsondata[i]['CompetitionID'])+"'"
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
                        FileMgr.CheckAndDownloadFile(key,value,4,Id)
                else:
                    FileMgr.CheckAndDownloadFile(key,value,4,Id)


                if 'Id' in key:
                    print('Record Added/Updated for '+tblName+' :'+str(value))

                if 'CompetitionMapping' in key:
                    insertOrUpdateRecord(value,'CompetitionBoxMapping',Id)
                else:
                    if 'CompetitionQuestions' in key and not 'CompetitionQuestionsOptions' in key:
                        insertOrUpdateRecord(value,'CompetitionQuestions',Id)
                    else:
                        if 'CompetitionQuestionsOptions' in key:
                            insertOrUpdateRecord(value,"CompetitionQuestionOptions",Id)
                        else:
                            if 'CompetitionWinners' in key:
                                insertOrUpdateRecord(value,"CompetitionWinner",Id)
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


imgpath = GetCMSData.GetData('Competitions')

insertOrUpdateRecord(imgpath,"Competition",None)

MoovahLogger.logger.info("Competitions updated successfully")