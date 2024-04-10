"""

Currently all this thing does is kick out a table telling when compress was last run.

"""
import sys
import os
#from logging.config import fileConfig
#logfile = sys.argv[1]
from flask import Flask, request
from app.sqlserver import ReadCompressionLog
from app.config import Config

application = Flask(__name__)

@application.route('/')
def f_html():
    """ Return output from lmstat """
    global r
    df = r.read()
    return df.to_html()

print("Starting web service.")
driver = "ODBC Driver 18 for SQL Server"
conn = f"Driver={driver};Server={Config.DBSERVER};Database={Config.DATABASE};uid={Config.DBUSER};pwd={Config.DBPASSWORD};Encrypt=No;"
r = ReadCompressionLog(conn)

# That's all!
