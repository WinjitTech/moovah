import sqlite3
import ConfReader
import SyncDBMgr as c


def altertable(strQuery, tnblname, columnList):
    # con = sqlite3.connect("khooloo.sqlite")
    con = sqlite3.connect(ConfReader.GetSyncDBPath())
    con.isolation_level = None
    c = con.cursor()
    strQuery = strQuery+tblname
    try:
        c.execute(strQuery)
        check_col = str(c.fetchall())
        for col in columnList:
            if col not in check_col:
                if col == "IsUserSpecific" or col == "IsRingFence":
                    alterQuery = "alter table" + tblname + "add column " + col + " INTEGER DEFAULT(0);"
                    c.execute(alterQuery)
                    print "Added column "+col+ " in" +tblname
                #if col not in check_col:
                else:
                    alterQuery = "alter table" + tblname + "add column " + col + " varchar2;"
                    c.execute(alterQuery)
                    print "Added column "+col+ " in" +tblname

    except Exception, e:
        print(str(e))

    finally:
        if con:
            con.close()

try:
    query = "CREATE TABLE IF NOT EXISTS 'UserTagging' ('Id' INTEGER PRIMARY KEY  NOT NULL , 'ModuleId' INTEGER, 'ReferenceId' INTEGER, 'MinAge' INTEGER DEFAULT -1, 'MaxAge' INTEGER DEFAULT -1, 'Gender' TEXT DEFAULT -1, 'EducationID' TEXT DEFAULT -1, 'MaritalStatusID' TEXT DEFAULT -1, 'NoOfDependents' TEXT DEFAULT -1, 'SalaryID' TEXT DEFAULT -1, 'EmploymentStatusID' TEXT DEFAULT -1, 'PreferenceID' TEXT DEFAULT -1, 'ProvinceID' TEXT DEFAULT -1, 'LanguageID' TEXT DEFAULT -1, 'ModifiedDate' TEXT)"
    c.execute(query)
    query = "CREATE TABLE IF NOT EXISTS 'SponsorLinking' ('Id' INTEGER PRIMARY KEY NOT NULL, 'ModuleId' INTEGER, 'ReferenceId' INTEGER, 'SponsorType' INTEGER, 'Type' TEXT, 'ModifiedDate' TEXT, 'Instructions' TEXT)";
    c.execute(query)
    query = ""
except Exception, e:
    print str(e)
# altertable("SELECT sql FROM sqlite_master WHERE tbl_name= 'Deals';")

tblname = "'Deals'"
columnList = ["CategoryId", "ReferenceId"]
altertable("SELECT sql FROM sqlite_master WHERE tbl_name=", tblname, columnList)

tblname = "'Survey'"
columnList = ["ProvinceID","IsRingFence", "UserIds"]
altertable("SELECT sql FROM sqlite_master WHERE tbl_name=", tblname, columnList)

tblname = "'Adverts'"
columnList = ["IsRingFence", "UserIds"]
altertable("SELECT sql FROM sqlite_master WHERE tbl_name=", tblname, columnList)



