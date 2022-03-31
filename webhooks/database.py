"""
    Create a connection to the SQL database using SQLAlchemy.
"""
import os
import sqlalchemy
import pandas as pd
import requests

class Database(object):

    def __init__(self, config):
        self.config = config
        url = sqlalchemy.engine.URL.create('sqlite3',
                                           database = self.config['DATABASE']
        )
        print(url)
        self.connection = sqlalchemy.create_engine(url)
        return



if __name__ == "__main__":

    # Test access to the SQL database using pandas.

    # The "V" means this is a view and
    # implies there is another table that has more photos?
    # I don't know why there are ACCT_ID and ACCOUNT_ID columns.
    from config import Config

    c = Config()._asdict()
    table = c['TEST']

    db = Database(c)
#    df = pd.read_sql(sql=query, con=db.connection)
#    print(df.info())
        
# Sample REST call https://cc-testmaps:9443/get_something?acct_id=26870
# Returns image name and date.
