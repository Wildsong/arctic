"""
Show information about the ArcGIS Enterprise datastores.
"""
import arcgis.gis.server
from config import Config
url = Config.SERVER_URL

url_admin = url + "/admin"
url_token = url + "/tokens/generateToken"

my_server = arcgis.gis.server.Server(
    url=url_admin,
#    token_url=url_token,
    username=Config.PORTAL_USER,
    password=Config.PORTAL_PASSWORD,
    all_ssl=True
)

my_ds_manager = arcgis.gis.server.DataStoreManager(
    url=my_server.url + "/data",
    gis=my_server
)


# Dump out a list of the datastores we know about.
datastores = my_ds_manager.list()
tick = 0
for ds in datastores:
    tick += 1
    print(tick, ds.properties['type'], end="")
    print(ds.properties)
    print()