"""
    The IIS Web Server logs traffic and keeps track of IP information,
    Esri does not, so we have to correlate the logs to get full information.
    This script gets information from IIS logs and puts it into our database.
"""
import os
import json
import datetime
from arcgis.gis import GIS

import database
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION

class ServerScan(object):

    def __init__(self) -> None:
        return

    def scan(self) -> None:

        return
    
if __name__ == '__main__':

    print("All done!")

