# arctic/datastore

Currently I am only interested in the "relational database" part of ArcGIS DataStore, which is actually a PostgreSQL server.

## General information

Most of this was gleaned by setting up an instance of pgadmin and just exploring the PostgreSQL databases.

## Broken admin tools (10.9)

I need to change the administrative user. The configureserviceaccount script fails. It says the credentials are wrong, and I do not agree.
The removemachine command would not work because cc-gisdatastore still thought it was the Primary. server/admin had a different opinion
so I used it and then just uninstalled the software on the VM.

I installed 10.9.1 on the VM and will leave it disconnected until I complete the upgrade to 10.9.1 on the old single machine deployment.

I need to change the mode on the tile caches (couchdb) because cc-gisdatastore is still marked as primary. I can't because the machine is
no longer reachable.

## Configuration

<ARCGISDATASTORE> for me is C:\arcgis\arcgisdatastore on the old machine and C:\arcgisdatastore on the new one. 

Configuration files are in <ARCGISDATASTORE>/

datastore.properties has a few settings in it, it's a plain text file.

The JSON files are the ones you want to read to get the information that comes from the describedatastore script.

arcgis-data-store-config.json -- folder locations, machine name, which features are turned on.

relational-config.json -- PostgreSQL server settings including role ("PRIMARY"), host name, port, a few stats like when it started

site-store-connection.json -- has the admin username and password in it

tilecache-config.json -- similar to the relational config


## Relational Store (PostgreSQL)

### Passwords for PostgreSQL

Log into the Datastore machine. In the Windows edition,

```bash
cd c:/Program Files/ArcGIS/DataStore/tools
./listadminusers
```

This will list several accounts, the one you need is the
"GDB Admin User". The default name for this account is the familiar "sde".

At this point you can try to connect using the psql command and use standard PostgreSQL commands, like this one which lists the databases that are on this server:

```bash
cd c:/Program Files/ArcGIS/DataStore/framework/runtime/pgsql/bin/
./psql -p 9876 -U sde -c "\l" postgres
Password for user sde:
```

The databases listed correspond with the entries found in the
config file C:\arcgisdatastore\etc\relational-config.json,
"datastore.admindb: dsadmindb" and "datastore.manageddb: db_0eoas".
There is also a setting "healthcheck.enable: true" in there, I wish I knew how that works.
Other settings that "describedatastore" exposes are in this file too, such as the start time, host name, status, etc.

The dsadmindb contains a few settings but nothing particularly exciting. The data is nearly all in the db_0eoas database.

### Remote access to the PostgreSQL database

Remote access has to be allowed by editing the pg_hba.conf file. It will be found on the datastore machine,
in the Windows edition it's in "C:/arcgisdatastore/pgdata/".

Edit the file to add a line like this. Use your own client IP address, not mine. Then restart the datastore service.
This will only allow the "sde" user to have access.

```bash
host all sde 10.10.10.210/32 scram-sha-256
```

While you are in the pg_hba.conf file, note that there are already a batch of entries created by ArcGIS to allow access 
replication servers if you have any. For example in my case there are entries for "cc-gis" on "cc-gisdatastore".
There are also IP address based entries (IPV4 and IPV6). I see entries for this machine too, cc-gisdatastore, not sure
when those get used.

The entries on my server allow access to the adm_077v5, hsu_9vn8j, and ins_nb0tr users.

### Interesting data

#### sde schema

The table "sde_layers" contains a row for each feature service with "table_name" column containing the name of each table in the hsu_9vn8j schema.

Other interesting tables might include:
gdb_items
gdb_itemtypes
sde_branches

There are 3 views here, db_tune, st_geometry_columns, and st_spatial_references.

There are about 10 triggers.

#### hsu_9vn8j schema

There is a table for each hosted service, so for example, the table "bus_stops_clatsop_routes" has a "shape" column holding the geometry, 
a bunch of attribute columns, including an "objectid" column. The "shape" column is of type "st_geometry" which is defined in the
schema sde types. I don't know how PostgreSQL "types" work yet.

There are views here too.

#### public schema

This schema has one table "sde_spatial_references" that appears to contain spatial reference system data. (False northings and eastings, etc etc.)


### PostgreSQL Replication

This server cc-gisdatastore should have replication set up with the other, cc-gis. I wonder where I'd see that?

I am assuming this is a SMR set up (Single Master), which means you can't update tables on the Standby server and expect them to show up on the Primary.

Replication is controlled by the postgresql.conf file, next door to the pg_hba.conf file in C:\arcgisdatastore\pgdata\.
On the standby server I see "primary_conninfo = "host=FQDN port=9876 user=dsrepuser password=SECRET"
where FQDN is the full server name and SECRET is a plain text password.

### How do I tell if replication works?

## Tile Cache (3D Scenes) (Couch database)

Also referred to as "nosqldb".

Config file: 

Couch Logs: <ARCGISDATASTORE>/logs/<MACHINNAME>/couchlog/couch.log

### CouchDB management

### Remote access to CouchDB

### CouchDB Replication

When operating with two servers there will be a Primary and Standby and there will be replication set up.

## Resources

[Esri documentation on datastore](https://enterprise.arcgis.com/en/data-store/latest/install/windows/data-store-utility-reference.htm)

### CouchDB

From the tilecache-config.json file I can see there is a web server running on port 29080/29081. If I hit that with a browser it shows me

There are more config settings in <ARCGISDATASTORE>/nosqldata/etc/*.ini

{"couchdb":"Welcome","version":"2.2.0","git_sha":"2a16ec4","features":["pluggable-storage-engines","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}

Commands available are here: https://docs.couchdb.org/en/2.3.1/
https://docs.couchdb.org/en/2.3.1/api/index.html


The admin page is at http://localho9st:20980/_utils
I don't know how to get access to it yet.


### PostgreSQL 

Tutorial on [PostgreSQL replication](https://www.enterprisedb.com/postgres-tutorials/postgresql-replication-and-automatic-failover-tutorial)

Official but not very readable [PostgreSQL docs on replication](https://www.postgresql.org/docs/13/runtime-config-replication.html)


