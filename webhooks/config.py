from logging import DEBUG
import os
from typing import NamedTuple

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(NamedTuple):
    """ 
In PRODUCTION conda sets up the environment,
so look in ~/.conda/envs/covid/etc/conda/activate.d/env_vars.sh
to see how it is set up. 

In development, we run in Flask so the environment comes from launch.json

Inheriting from a NamedTuple allows access the attributes either with dict or dotted object notation.
    """
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or "12345678"

    APP_SERVER_URL: str = "https://apps.co.clatsop.or.us/property"
    STATIC_HOST: str = "https://giscache.co.clatsop.or.us"
    if os.environ.get('FLASK_ENV') == 'development':
        STATIC_HOST = "https://127.0.0.1:9443"

    DB_SERVER: str = os.environ.get('DB_SERVER')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
    DATABASE: str = os.environ.get('DATABASE')
    PHOTO_TABLE: str = 'atuser.AT_V_PRIMARY_ACCT_PHOTO'

    BOT_NAME = os.environ.get("BOT_NAME")
    BOT_USER = os.environ.get("BOT_USER")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

    pass

    @staticmethod
    def init_app(app):
        # This gets called from the app __init__.
        pass


if __name__ == "__main__":

    config = Config()

    print(config._asdict())

    assert config.SECRET_KEY

    # These have to be defined in your environment
    # for example in a .env file or launch.json
    # or conda environment.

    assert config.APP_SERVER_URL
    assert config.STATIC_HOST
    assert config.PHOTO_TABLE
    assert config.DB_SERVER
    assert config.DB_USER
    assert config.DB_PASSWORD
    assert config.DATABASE

    assert config.BOT_NAME
    assert config.BOT_USER
    assert config.BOT_TOKEN
    assert config.CHAT_ID
    pass

# That's all!
