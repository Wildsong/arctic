import os
from arcgis.gis import GIS
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION


if __name__ == "__main__":

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    log = gis.admin.logs

    server_manager = gis.admin.servers
    server = server_manager.list()[0]

    dsm = server.datastores

    # Docs say all parameters are optional but that is wrong.
    items = dsm.search(types='folder,egdb,datadir')['items']
    for d in items:
        for k,v in d.items():
            if k=='provider' and v=='ArcGIS Data Store':
                machines = d['info']['machines']
                print('machines:')
                for machine in machines:
                    print("  name: %s role:%s" % (machine['name'],machine['role']))
            if k=='info':
                print(" info")
                for k,v in v.items():
                    print('   %s :' % k, v)
            else:
                print(' %s :' % k, v)
        print()
# update logging settings

    # for portal, datastore, server
    # grab log

    # parse it
    # show interesting messages

    print("That's all!")
