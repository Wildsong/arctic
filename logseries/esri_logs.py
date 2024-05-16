import os
import re
from datetime import datetime, timezone
from dateutil import tz
from glob import glob
import pandas as pd
from arcgis.gis import GIS
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION

# What I want from the log right now
# time
# type
# code
re_log = re.compile(r'time=\"(\S+),(\S+)\" type=\"(\S+)\" code=\"(\S+)\" source=\"(\S+)\"')


def showDict(d_log: dict) -> None:
    for k, v in d_log.items():
        print('  ', k, v)
    return

def parseWebLog(pathname: str) -> list:
    """Parse an IIS web server log file

    Args:
        pathname (str): Path of the file

    Returns:
        list: JSON formatted messages
    """

    # This is the list of names for each field read from the log.
    # The number of fields has to match the # of columns in the log entries.
    fieldnames = [
        #'date', # we roll date and time into one field so skip this one
        'time',
        'name',
        's_ip',
        'method',
        'cs_uri_stem',
        'cs_username',
        's_port',
        'empty',
        'c_ip',
        'userAgent',
        'referer',
        'sc_status',
        'sc_substatus',
        'huh',
        'time_taken',
    ]
    results = list()
    with open(pathname, "r") as fp:
        d = dict()
        for item in fp:
            if item[0] == '#':
                continue
            # strip off the newline and tokenize based on space as a delimiter
            fields = item.strip().split(' ')
            i = 0

            logtime = fields[0] + ' ' + fields[1]
            dtutc = datetime.fromisoformat(logtime).replace(tzinfo=timezone.utc)
            fields[1] = dtutc
            del fields[0]

            for field in fields:
                d[fieldnames[i]] = field
                i += 1
            
            results.append(d)
    return results

def parseEsriLog(pathname: str, level:list=None, code:list=None) -> list:
    """Parse an Esri log file (for example, from ArcGIS Server in the server/ folder.)

    Args:
        pathname (str): path to the text file
        level (list, optional): List of logging levels that are of interest, like WARNING or SEVERE. Defaults to None.
        code (list, optional): List of error codes to watch for. Codes are 4-digit integers. Defaults to None.

    Returns:
        list: A summary in JSON format
    """
    tzlocal = tz.gettz('Americas/Los_Angeles')
    results = list()
    # Esri log files are in mock XML format, and each entry is on a single line.
    # I could probably use some dandy XML parser but this is easier.
    with open(pathname, "r") as fp:
        for item in fp:
            mo = re_log.search(item)
            if mo:
                l = mo.group(3)
                c = int(mo.group(4))
                s = mo.group(5)
                if ((not level) or (l in level)) and ((not code) or (code and c in code)):
                    t = datetime.fromisoformat(mo.group(1)).replace(tzinfo=tzlocal)
                    utc = t.astimezone(timezone.utc).replace(microsecond=0, second=0)
                    # I wonder if source or requestId are of any use to us?
                    results.append({"time":utc, "type":l, "code":c, "source":s})
    return results

class LogProcessor(object):
    def __init__(self, gis):
        self.gis = gis
        return

##    https://delta.co.clatsop.or.us/server/admin/logs/query?startTime=&endTime=&level=WARNING&filterType=json&filter=%7B%22codes%22%3A%5B%5D%2C%0D%0A%22processIds%22%3A%5B%5D%2C%0D%0A%22requestIds%22%3A%5B%22%22%5D%2C%0D%0A%22server%22%3A+%5B%22SERVER%22%5D%2C%0D%0A%22services%22%3A+%22*%22%2C%0D%0A%22machines%22%3A+%5B%22CC-GISSERVER.CLATSOP.CO.CLATSOP.OR.US%22%5D%7D&pageSize=1000&f=html

    def findLogs(self):
        """Figure out the locations of the various logs and stash them in this object.
        """        
        # Rewrite the log pathnames to reference network locations instead of local folders.
        l_logdir = {
            "C:\\arcgis\\arcgisportal\\logs\\" : '//cc-gis/C$/arcgis/arcgisportal/logs/',
            "C:\\arcgisserver\\logs\\" : '//cc-gisserver/C$/arcgisserver/logs/',
        }
        for item in l_logdir.items():
            assert(os.path.exists(item[1]))

        print("Web Server")
        logDir = '//cc-gis/C$/inetpub/logs/LogFiles/W3SVC'
        logFiles = sorted(glob(logDir + '/u_*.log'), key=os.path.getmtime)
    #    for log in logFiles:
    #        print(log)
        latest = logFiles[-1] 
        print(f"Latest web log file is {latest}")
        self.webLogFile = latest

        print("Portal")
        d_log = gis.admin.logs.settings
        d_log['logDir'] = l_logdir[d_log['logDir']]
        showDict(d_log)

        print("Server")
        server_manager = gis.admin.servers
        server = server_manager.list()[0] # You can have many servers managed by one Portal but we don't
        d_log = server.logs.settings
        d_log['logDir'] = l_logdir[d_log['logDir']]
        showDict(d_log)

        logDir = d_log['logDir'] + '/' + SERVER_NAME + '/server'
        assert(os.path.exists(logDir))
        logFiles = sorted(glob(logDir + '/*.log'), key=os.path.getmtime)
    #    for log in logFiles:
    #        print(log)
        latest = logFiles[-1] 
        print(f"Latest server log file is {latest}")
        self.serverLogFile = latest

        # There is no API for this.
        # You can run describedatastore on the datastore machine though.
        print("Datastore")
        datastore_logs = {
            "logDir": '//cc-gisdatastore/C$/arcgisdatastore/logs/CC-GIS.CLATSOP.CO.CLATSOP.OR.US',
            "logLevel": "unknown"
        }
        showDict(datastore_logs)

        return
    
    def loadWebLog(self):
        dlog = parseWebLog(self.webLogFile)
        self.webLog = pd.DataFrame.from_dict(dlog, orient='columns')
        print(self.webLog)
        return

    def loadServerLog(self):
        dlog = parseEsriLog(self.serverLogFile)
        self.serverLog = pd.DataFrame.from_dict(dlog, orient='columns')
        print(self.serverLog)
        return

# UNIT TESTS

def logParseTest() -> None:    
    # Read some stashed log files to test parsers
    serverlog = 'logseries/server-20240418.134616-11028-0.0.log'
    weblog = 'logseries/u_ex240515.log'
    log0 = parseWebLog(weblog)
    log1 = parseEsriLog(serverlog, level=["WARNING"], code=[9040])
    log2 = parseEsriLog(serverlog, level=["WARNING", "SEVERE"], code=[9040, 9002])
    log3 = parseEsriLog(serverlog, level=["SEVERE"], code=[9001, 9002])
    print(log0[-1])
    print(log3[-1])
    print(len(log0), len(log1), len(log2), len(log3))

if __name__ == "__main__":

    SERVER_NAME = 'CC-GISSERVER.CLATSOP.CO.CLATSOP.OR.US'
#    logParseTest()

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    lp = LogProcessor(gis)
    lp.findLogs()

    # Load the logs into dataframes
    lp.loadWebLog()
    lp.loadServerLog()

    wi = lp.webLog.set_index('time')
    si = lp.serverLog.set_index('time')

    # Now, try to join them.
#    df = si.join(wi, how='left', lsuffix='_esri', rsuffix='_web')
    df = wi.join(si, how='left', lsuffix='_esri', rsuffix='_web')
    print(df)

# Update logging settings

    print("That's all!")
