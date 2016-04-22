import sqlite3
import SyncDBMgr as c
import GetCMSData
import FileMgr
import ConfReader
import MoovahLogger


def insertOrUpdateRecord(jsondata, tblName, ParentID):
    if 'DealsBoxMapping' in tblName and ParentID is not None:
        query = "delete from " + tblName + " where DealID='" + str(ParentID) + "'"
        print('Records deleted for ' + tblName + ' for DealID :' + str(ParentID))
        c.execute(query)

    for i in range(len(jsondata)):
        Id = jsondata[i]['Id']

        query = "delete from " + tblName + " where Id='" + str(Id) + "'"

        c.execute(query)

        if "BoxID" in jsondata[i].keys() and "DealID" in jsondata[i].keys():
            query = "delete from " + tblName + " where BoxID='" + str(
                jsondata[i]['BoxID']) + "'" + " and DealID='" + str(jsondata[i]['DealID']) + "'"
            print('Record deleted for ' + tblName + ' :' + str(Id))
            c.execute(query)

        if "RetailerBranchID" in jsondata[i].keys() and "DealID" in jsondata[i].keys():
            query = "delete from " + tblName + " where RetailerBranchID='" + str(
                jsondata[i]['RetailerBranchID']) + "'" + " and DealID='" + str(jsondata[i]['DealID']) + "'"
            print('Record deleted for ' + tblName + ' :' + str(Id))
            c.execute(query)

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

                # Check if it is a file to download and download it.
                if "IsActive" in jsondata[i].keys():
                    if jsondata[i]["IsActive"] == 1:
                        FileMgr.CheckAndDownloadFile(key, value, 2, Id)
                else:
                    FileMgr.CheckAndDownloadFile(key, value, 2, Id)

                if 'Id' in key:
                    print('Record Added/Updated for ' + tblName + ' :' + str(value))

                if 'DealLocations' in key:
                    insertOrUpdateRecord(value, 'DealLocations', Id)
                else:
                    if 'DealMappings' in key:
                        insertOrUpdateRecord(value, "DealsBoxMapping", Id)
                    else:
                        if value is not None:
                            cols = cols + key + ','
                            vals = vals + '"' + str(value) + '",'

            query += cols[:-1] + ') values(' + vals[:-1] + ');'
            c.execute(query)

        # print(query)

        except Exception, e:
            print 'Insert Error for [' + tblName + '] id=' + str(Id) + ' details:' + str(e)
            continue


imgpath = GetCMSData.GetData('Deals')

insertOrUpdateRecord(imgpath, "Deals", None)

MoovahLogger.logger.info("Deals updated successfully")
