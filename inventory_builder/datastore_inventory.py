import os
from arcgis.gis import GIS
from config import Config

VERSION = '1.0'
path, exe = os.path.split(__file__)
myname = exe + ' ' + VERSION


if __name__ == "__main__":

    gis = GIS(Config.PORTAL_URL, Config.PORTAL_USER, Config.PORTAL_PASSWORD)
    pds = gis.datastore

    ds_items = gis.content.search('*', item_type="Data Store")
    for item in ds_items:
        d = item.get_data()
        print(f"{item['title']} Type:{d['type']}")
        if d['type']=='egdb':
            layers = pds.layers(item) # nothing to see here unless you use publish_layers
            for layer in layers:
                print(layer)
   
    print("That's all!")
