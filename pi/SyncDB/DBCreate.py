import sqlite3
import ConfReader
import SyncDBMgr as c

try:

    query = "CREATE TABLE IF NOT EXISTS 'UserTagging' ('Id' INTEGER PRIMARY KEY  NOT NULL , 'ModuleId' INTEGER, 'ReferenceId' INTEGER, 'MinAge' INTEGER DEFAULT -1, 'MaxAge' INTEGER DEFAULT -1, 'Gender' TEXT DEFAULT -1, 'EducationID' TEXT DEFAULT -1, 'MaritalStatusID' TEXT DEFAULT -1, 'NoOfDependents' TEXT DEFAULT -1, 'SalaryID' TEXT DEFAULT -1, 'EmploymentStatusID' TEXT DEFAULT -1, 'PreferenceID' TEXT DEFAULT -1, 'ProvinceID' TEXT DEFAULT -1, 'LanguageID' TEXT DEFAULT -1, 'ModifiedDate' TEXT)"
    c.execute(query)
    query = "CREATE TABLE IF NOT EXISTS 'SponsorLinking' ('Id' INTEGER PRIMARY KEY NOT NULL, 'ModuleId' INTEGER, 'ReferenceId' INTEGER, 'SponsorType' INTEGER, 'Type' TEXT, 'ModifiedDate' TEXT, 'Instructions' TEXT)";
    c.execute(query)
except Exception, e:
    print str(e)
