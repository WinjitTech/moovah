#!/usr/bin/python

import cgi
import json
import sqlite3

import sqliteUtilities
import ConfReader

form = cgi.FieldStorage()

lastSyncDateTime = (form.getvalue('lastSyncDateTime'))

#lastSyncDateTime= "2016-03-29T09:08:25.763" #datetime.datetime.now()

#UserId = 117511

response ={}

response['StatusCode']=200
response['ErrorDetails']=None
response['IsNextPageExists']=False
response['NextPageLink']=""

print "Content-type: application/json\n\n"


try:
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    db = sqlite3.connect(ConfReader.GetSyncDBPath())

    db.row_factory = sqliteUtilities.dict_factory

    c = db.cursor()

    c.execute("select Id ,Name ,Tagline ,Description ,SurveyType ,TotalQuestions ,Path ,AdditionalPath ,StartDate ,EndDate ,TimeInHours ,IsGeneral ,Gender ,EducationID ,MaritalStatusID ,NoOfDependents ,SalaryID ,EthnicID ,EmploymentStatusID ,Sponsor ,FileName ,SponsorImage ,SponsorLink ,IsActive ,ModifiedDate ,MinAge ,MaxAge ,IsOpenSurvey ,AvailableLimit ,IsBoxData ,IsGPS ,GPSLocations ,Radius ,Price ,PreferenceID ,LanguageID ,ImagePath,ProvinceID from Survey where ModifiedDate > '" + (lastSyncDateTime) + "' and ( isRingFence=0 or isRingFence is not null);")
    #c.execute("select * from Survey where UserIds like '%,127520,%' and isRingFence=0 and ModifiedDate > '2016-03-11T12:16:42.717';")


    results = c.fetchall()

    for result in results:
        strQuery = "select * from SurveyBoxMapping where SurveyID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['SurveyMapping'] = results2

    for result in results:
        strQuery = "select * from SurveyQuestions where SurveyID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()

        for result2 in results2:
            strQuery = "select * from SurveyQuestionOptions where QuestionID = " + str(result2['Id'])
            c.execute(strQuery)
            results3 =c.fetchall()
            result2['SurveyQuestionsOptions'] = results3

        result['SurveyQuestions'] = results2


    response['ReturnObject'] = results


    print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
        response = {'result': str(e)}



#print json.JSONEncoder().encode(response)

