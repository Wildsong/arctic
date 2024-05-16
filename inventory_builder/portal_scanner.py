"""
    The Portal keeps lots of information about its contents,
    this script gets information from it and puts it into our database.
"""
import database

import os
import json
from arcgis.gis import GIS
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION


def scan_portal():

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    log = gis.admin.logs

    server_manager = gis.admin.servers
    server = server_manager.list()[0]

    print("Services:")
    service_manager = server.services
    folders = service_manager.folders

    broken_services = list()
    stopped_services = list()

    ts = 0
    print("Folders: %d" % len(folders))
    fcount = 0
    i = 0

    for f in folders:
        l = service_manager.list(folder=f)
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

    print("That's all!")

# update logging settings

    # for portal, datastore, server
    # grab log

    # parse it
    # show interesting messages

if __name__ == "__main__":
    scan_portal()
    print("All done! That was SOOOO fast!")

