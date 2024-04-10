"""
    The GIS Server keeps lots of information about its contents,
    this script gets information from it and puts it into our database.
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

    def __init__(self, gis) -> None:
        self.gis = gis
        pass

    def scan(self) -> None:

        # https://developers.arcgis.com/python/api-reference/arcgis.gis.server.html#servermanager
        server = self.gis.admin.servers
        allmyservers = server.list()

        # I can't do a lot of development work here because I am poor and have just the one server!
        # I can only try.
        for s in allmyservers:
            self.scan_server(s)        

    def scan_server(self, server) -> None:
        """ Scan a single server. """

        self.logs(server.logs)
        self.services(server.services)

    def services(self, services) -> None:
        print("Services:")
        folders = services.folders

        broken_services = list()
        stopped_services = list()

        ts = 0
        print("Folders: %d" % len(folders))
        fcount = 0
        i = 0

        for f in folders:
            l = services.list(folder=f)
            print("Folder [%d] %s: %d" % (fcount, f, len(l)))
            fcount += 1
            
            # We're not in charge of these!
            if f == 'System':
                continue

            for service in l:
                print("Service [%d]:" % i)
                i += 1

                status = service.status
                if 'status' in status:
                    broken_services.append(service)
                    continue

                state = status['configuredState']
                if state == 'STOPPED':
                    stopped_services.append(service)
                    continue

                print("  name: \"%s\" %s %s" % (service.serviceName, service.type, state))

                if service.type == 'GPServer':
                    continue

                props = service.properties

                if "portalProperties" not in props:
                    continue

                continue

                pprops = props.portalProperties
                pi = 0
                for item in pprops.portalItems:
                    print("  portal item [%d] %s %s" %
                        (pi, item.itemID, item.type))
                    # query portal for more information
                    pi += 1

        print("total services", i)

        print()
        print("Broken services:")
        for service in broken_services:
            print("  URL", service.url)
            #print(service.status['messages'])

        print("Stopped services:")
        i = 0
        for service in stopped_services:
            print("  name: \"%s\" %s" % (service.serviceName, service.type))
            i += 1

        return
    
    def logs(self, log) -> None:
        """ Collect log information """

        # https://developers.arcgis.com/python/api-reference/arcgis.gis.server.html#logmanager

        print("Log level:", log.settings['logLevel'])
        print("Log directory:", log.settings['logDir'])

        print("Crash reports:", log.count_error_reports(), "max:", log.settings['maxErrorReportsCount']) 
        # 2024-03-08 I changed this from 10 to 100 because 10 kind of masks any real problem.

        # The files generated are in "Mini DuMP" format (binary) files
        # but the name of the file matches the service that crashed.
        # If you really want, you can look at the file contents with a tool called
        # BlueScreenView from https://www.nirsoft.net/utils/blue_screen_view.html

        
        # Stuff I could do here --
        # I can clear logs -- clean just removes ALL the log files! Tsk.
        # I can change the log level
        # I can query logs for interesting tidbits like say SEVERE errors
        # I could just import a date range into a database table
        # like maybe the last 24 hours?
        # What's a good way to aggregate and analyze logs? 
        # Examine ArcGIS Monitor docs. If they exist.

        # Let's just try to look at 24 hours of logs
        start = datetime.datetime.now() - datetime.timedelta(days=1)

        # You can tell this method to generate a file if you want.
        logdict = log.query(start_time=start, since_server_start=False, level="SEVERE", max_records_return=1000)
        for entry in logdict['logMessages']:
            unixtime = int(entry['time']) / 1000
            ts = datetime.datetime.utcfromtimestamp(unixtime).strftime("%Y-%m-%d %H:%M:%S")
            machine = entry['machine'] # I need to truncate this
            print(f"{ts} {entry['source']} {machine} {entry['message']}")

        return
    

if __name__ == "__main__":

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    server = ServerScan(gis)
    server.scan()
    #server.logging() ??????

    print("All done!")
