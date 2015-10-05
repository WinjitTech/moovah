#!/usr/bin/python

import cgi
import json
import sqlite3
import sys
import sqliteUtilities
import ConfReader

postData={}
postData = sys.stdin.read()

if postData is not None or postData is not '':
    postData =json.loads(postData)

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

    Result={}
    Result["IsAlbums"]=False
    Result["IsApps"]=False
    Result["IsArticles"]=False
    Result["IsNewsFeeds"]=False
    Result["IsSurveys"]=False
    Result["IsCompetitions"]=False
    Result["IsDeals"]=False
    Result["IsCategories"]=False
    Result["IsSubCategories"]=False
    Result["IsPreferences"]=False
    Result["IsAdverts"]=False
    Result["IsBannerImages"]=False
    Result["IsBox"]=False
    Result["IsSponsors"]=False
    Result["IsRetailers"]=False
    Result["IsRoutes"]=False
    Result["IsContentOwners"]=False
    Result["IsCreditRules"]=False
    Result["IsTermsAndConditions"]=False
    Result["IsGeneralSettings"]=False
    Result["IsLocation"]=False

    i=0
    for kval in postData:

        if kval["Key"] == "Albums":
            c.execute("select * from Album where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsAlbums"]=True
                break

        if kval["Key"] == "Apps":
            c.execute("select * from Apps where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsApps"]=True
                break

        if kval["Key"] == "Articles":
            c.execute("select * from Article where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsArticles"]=True
                break

        if kval["Key"] == "NewsFeeds":
            c.execute("select * from rss where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsNewsFeeds"]=True
                break

        if kval["Key"] == "Surveys":
            c.execute("select * from survey where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsSurveys"]=True
                break

        if kval["Key"] == "Competitions":
            c.execute("select * from Competition where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsCompetitions"]=True
                break

        if kval["Key"] == "Deals":
            c.execute("select * from deals where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsDeals"]=True
                break

        if kval["Key"] == "Categories":
            c.execute("select * from category where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsCategories"]=True
                break

        if kval["Key"] == "SubCategories":
            c.execute("select * from SubCategory where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsSubCategories"]=True
                break

        if kval["Key"] == "Preferences":
            c.execute("select * from Preferences where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsPreferences"]=True
                break

        if kval["Key"] == "Adverts":
            c.execute("select * from Adverts where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsAdverts"]=True
                break

        if kval["Key"] == "BannerImages":
            c.execute("select * from BannerImages where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsBannerImages"]=True
                break

        if kval["Key"] == "Box":
            c.execute("select * from box where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsBox"]=True
                break

        if kval["Key"] == "Sponsors":
            c.execute("select * from Sponsor where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsSponsors"]=True
                break

        if kval["Key"] == "Retailers":
            c.execute("select * from Retailer where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsRetailers"]=True
                break

        if kval["Key"] == "Routes":
            c.execute("select * from Route where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsRoutes"]=True
                break

        if kval["Key"] == "ContentOwners":
            c.execute("select * from ContentOwner where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsContentOwners"]=True
                break

        if kval["Key"] == "CreditRules":
            c.execute("select * from CreditRule where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsCreditRules"]=True
                break

        if kval["Key"] == "TermsAndConditions":
            c.execute("select * from TermsAndConditions where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsTermsAndConditions"]=True
                break

        if kval["Key"] == "GeneralSettings":
            c.execute("select * from GeneralSetting where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsGeneralSettings"]=True
                break

        if kval["Key"] == "Location":
            c.execute("select * from Locations where ModifiedDate > '" + (kval["LastSyncDateTime"]) + "';")
            for rec in c.fetchall():
                Result["IsLocation"]=True
                break


    response['ReturnObject'] = [Result]

    #print json.JSONEncoder().encode(response)

except Exception,e:
        with open("PythonErrors.txt", "a") as myfile:
            myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
        response = {'result': str(e)}

print json.JSONEncoder().encode(response)

