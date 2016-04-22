import sys
import getopt
import FillReports
import GetCMSData
import datetime
import MoovahLogger

try:
    # sys.argv = ['postBoxDetailsOncms.py', '--BoxID="40"']
    # sys.argv = ['SyncDataFile.py', '--CleanDB=0']

    opts, args = getopt.getopt(sys.argv[1:], 'h:', ["CleanDB="])
except getopt.GetoptError:
    print 'SyncDataFile.py [--CleanDB=1] '
    sys.exit(2)

CleanDB = '0'

for opt, arg in opts:
    if opt == '--CleanDB':
        CleanDB = arg

if CleanDB is '1':
    GetCMSData.CleanDatabaseFile()
    print 'Database file cleaned successfully'

d = datetime.datetime.now()
DateTimeSyncStarted = d.strftime('%Y-%m-%d %H:%M:%S')

try:
    GetCMSData.GetDataFromCMS()
    print 'Database file downloaded successfully'
    MoovahLogger.logger.info("Sync data file updated successfully")
    FillReports.InsertIntoboxsyncdatalog(DateTimeSyncStarted, '', 0, '')
except Exception, e:
    print "Sync data file update failed : " + str(e)
    MoovahLogger.logger.info("Sync data file update failed : " + str(e))
    d = datetime.datetime.now()
    DateTimeSyncStoped = d.strftime('%Y-%m-%d %H:%M:%S')
    FillReports.InsertIntoboxsyncdatalog(DateTimeSyncStarted, DateTimeSyncStoped, 0, '')
