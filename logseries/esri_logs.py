import os
import re
from arcgis.gis import GIS
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION


def showLogSettings(d_log: dict) -> None:
    for k, v in d_log.items():
        print('  ', k, v)

# What I want from the log right now
# time
# type
# code
re_log = re.compile(r'time=\"(\S+),(\S+)\" type=\"(\S+)\" code=\"(\S+)\"')

def parse_log(pathname, level=None, code=None) -> list():
    """ Parse an Esri log file. Return json. """

    results = list()

    # Esri log files are in mock XML format, and each entry is on a single line.
    # I could probably use some dandy XML parser but this is easier.
    with open(pathname, "r") as fp:
        for item in fp:
            mo = re_log.search(item)
            if mo:
                l = mo.group(3)
                c = int(mo.group(4))
                if l in level and c in code:
                    results.append({"time":mo.group(1), "code":c})
    return results

# UNIT TESTS
if __name__ == "__main__":

    logdir = '//cc-gis/C$/arcgisserver/logs/CC-GIS.CLATSOP.CO.CLATSOP.OR.US/server'
    
    serverlog = 'logseries/sample.log'
    log1 = parse_log(serverlog, level=["WARNING"], code=[9040])
    log2 = parse_log(serverlog, level=["WARNING", "SEVERE"], code=[9040, 9002])
    log3 = parse_log(serverlog, level=["SEVERE"], code=[9001, 9002])

    print(len(log1), len(log2), len(log3))

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    d_log = gis.admin.logs.settings

    print("Portal")
    showLogSettings(d_log)

    server_manager = gis.admin.servers
    server = server_manager.list()[0]

    print("Server")
    showLogSettings(server.logs.settings)

    # There is no API for this.
    # You can run describedatastore on the datastore machine though.
    # That's how I got this information.
    print("Datastore")
    datastore_logs = {
        "logDir": "C:\\arcgis\\arcgisdatastore\\logs\\",
        "logLevel": "unknown"
    }
    showLogSettings(datastore_logs)

# I wonder how I'd know what machine to look at?
# whatever not what I am after here is it now?

# update logging settings

    # for portal, datastore, server
    # grab log

    # parse it
    # show interesting messages

    print("That's all!")
