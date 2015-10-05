#!/usr/bin/python

import cgi
import json
import sqlite3

import sqliteUtilities
import ConfReader

form = cgi.FieldStorage()

lastSyncDateTime = (form.getvalue('lastSyncDateTime'))

#lastSyncDateTime= "0001-01-01 00:00:00.000" #datetime.datetime.now()

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


    c.execute("select * from Competition where ModifiedDate > '" + (lastSyncDateTime) + "';")


    results = c.fetchall()

    for result in results:
        strQuery = "select * from CompetitionBoxMapping where CompetitionID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['CompetitionMapping'] = results2

    for result in results:
        strQuery = "select * from CompetitionQuestions where CompetitionID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()

        for result2 in results2:
            strQuery = "select * from CompetitionQuestionOptions where QuestionID = " + str(result2['Id'])
            c.execute(strQuery)
            results3 =c.fetchall()
            result2['CompetitionQuestionsOptions'] = results3

        result['CompetitionQuestions'] = results2

    for result in results:
        strQuery = "select * from CompetitionWinner where CompetitionID = " + str(result['Id'])
        c.execute(strQuery)
        results2 =c.fetchall()
        result['CompetitionWinners'] = results2


    response['ReturnObject'] = results


    print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
        response = {'result': str(e)}



#print json.JSONEncoder().encode(response)
