import urllib
import httplib2
import os
import urlparse
import commands
from posixpath import dirname
import datetime
import MoovahLogger
import sys
import FillReports


def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("%2d%%" % percent)
      sys.stdout.write("\b\b\b")
      sys.stdout.flush()

def CheckURLStatus(url):
    try:
        h = httplib2.Http()#res = conn.getresponse()
        resp = h.request(url, 'HEAD')
        status = resp[0]['status']
        return status
    except Exception,e:
        MoovahLogger.logger.debug("Remote File Error:=> "+str(e))
        return '500'


def DownloadFileToPath(RemotePath,LocalPath):
    try:
        status = CheckURLStatus(RemotePath)
        if status == "200":
            testfile = urllib.URLopener()
            commands.getoutput("mkdir -p "+dirname(LocalPath))
            if os.path.exists(LocalPath):

                SizeRemote = int(urllib.urlopen(RemotePath).info().getheaders("Content-Length")[0])
                SizeLocal = os.path.getsize(LocalPath)
                if not (SizeLocal==SizeRemote):
                    testfile.retrieve(RemotePath, LocalPath,reporthook=dlProgress)
                    print(" File Downloaded to: "+LocalPath)
                    MoovahLogger.logger.info("File Downloaded to: "+LocalPath)
            else:
                testfile.retrieve(RemotePath, LocalPath,reporthook=dlProgress)
                print(" File Downloaded to: "+LocalPath)
                MoovahLogger.logger.info("File Downloaded to: "+LocalPath)

        if os.path.exists(LocalPath):
            return True
        else:
            return False

    except Exception,e:
        MoovahLogger.logger.error("Download File Error:=> "+str(e))
        return False

def DownloadFileToPath(RemotePath,LocalPath,SectionEnumVal,RecordID):
    try:
        status = CheckURLStatus(RemotePath)
        if status == "200":
            SizeRemote = int(urllib.urlopen(RemotePath).info().getheaders("Content-Length")[0])
            testfile = urllib.URLopener()
            commands.getoutput("mkdir -p "+dirname(LocalPath))
            if os.path.exists(LocalPath):
                SizeLocal = os.path.getsize(LocalPath)
                if not (SizeLocal==SizeRemote):
                    testfile.retrieve(RemotePath, LocalPath,reporthook=dlProgress)
                    FillReports.InsertIntoboxsyncdetailslog(RemotePath,1,'',RecordID,SizeRemote,SectionEnumVal)
                    print(" File Downloaded to: "+LocalPath)
                    MoovahLogger.logger.debug("File Downloaded to: "+LocalPath)
            else:
                testfile.retrieve(RemotePath, LocalPath,reporthook=dlProgress)
                FillReports.InsertIntoboxsyncdetailslog(RemotePath,1,'',RecordID,SizeRemote,SectionEnumVal)
                print(" File Downloaded to: "+LocalPath)
                MoovahLogger.logger.debug("File Downloaded to: "+LocalPath)
        else:
            FillReports.InsertIntoboxsyncdetailslog(RemotePath,0,'CMS Error Code: '+str(status),RecordID,0,SectionEnumVal)

        if os.path.exists(LocalPath):
            return True
        else:
            return False

    except Exception,e:
        FillReports.InsertIntoboxsyncdetailslog(RemotePath,0,'Internet connection not avialable',RecordID,SectionEnumVal)
        MoovahLogger.logger.debug("Download File Error:=> "+str(e))
        return False


def CheckAndDownloadFile(key,RemoteURL):

    try:

        ContentTokens =[

            "AdvertPath",
            "ThumbnailPath",
            "SponsorImage",
            "ImagePath",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Path",
            "IconImage",
            "ScreenShot1",
            "ScreenShot2",
            "ScreenShot3",
            "ScreenShot4",
            "ScreenShot5",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Logo",
            "BannerPath",
            "TCPath",
            "ExtraContent",
            "BannerImage",
            "FullScreenImage",
            "AdditionalPath",
            "BuildPath",
            "BannerLink"

        ]

        #LocaPath ="/media/usb0/moovah"
        LocaPath ="/home/pi"

        if key in ContentTokens and RemoteURL is not None and RemoteURL is not '':
            parse_object = urlparse.urlparse(RemoteURL)
            LocaPath+=parse_object.path
            RemoteURL = str(RemoteURL).replace(".net",".com")

            if ".mp4" in RemoteURL:

                if not DownloadFileToPath(str(RemoteURL[:-3]+"3gp"),str(LocaPath[:-3]+"3gp")):
                    print("File Downloaded Failed for: "+str(LocaPath[:-3]+"3gp"))

                if not DownloadFileToPath(RemoteURL,LocaPath):
                    print("File Downloaded Failed for: "+LocaPath)

            else:
                if not DownloadFileToPath(RemoteURL,LocaPath):
                    print("File Downloaded Failed for: "+LocaPath)

    except Exception,e:
        MoovahLogger.logger.error("Debug: " +"executed at :" +str(e))


def CheckAndDownloadFile(key,RemoteURL,SectionEnumVal,RecordID):

    try:

        ContentTokens =[

            "AdvertPath",
            "ThumbnailPath",
            "SponsorImage",
            "ImagePath",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Path",
            "IconImage",
            "ScreenShot1",
            "ScreenShot2",
            "ScreenShot3",
            "ScreenShot4",
            "ScreenShot5",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Logo",
            "BannerPath",
            "TCPath",
            "ExtraContent",
            "BannerImage",
            "FullScreenImage",
            "AdditionalPath",
            "BuildPath",
            "BannerLink"

        ]

        #LocaPath ="/media/usb0/moovah"
        LocaPath ="/home/pi"

        if key in ContentTokens and RemoteURL is not None and RemoteURL is not '':
            parse_object = urlparse.urlparse(RemoteURL)
            LocaPath+=parse_object.path
            RemoteURL = str(RemoteURL).replace(".net",".com")

            if ".mp4" in RemoteURL:

                if not DownloadFileToPath(str(RemoteURL[:-3]+"3gp"),str(LocaPath[:-3]+"3gp"),SectionEnumVal,RecordID):
                    print("File Downloaded Failed for: "+str(LocaPath[:-3]+"3gp"))

                if not DownloadFileToPath(RemoteURL,LocaPath,SectionEnumVal,RecordID):
                    print("File Downloaded Failed for: "+LocaPath)

            else:
                if not DownloadFileToPath(RemoteURL,LocaPath,SectionEnumVal,RecordID):
                    print("File Downloaded Failed for: "+LocaPath)

    except Exception,e:
        MoovahLogger.logger.error("Debug: " +"executed at :" +str(e))

#CheckAndDownloadFile("Path","http://moovahapp.net/Live/Shared/MediaFiles/Video/from_jack_to_juke__a_history_of_ghetto_house/icon.png")