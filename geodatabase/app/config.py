import os

def file_must_exist(f):
    if os.path.exists(f): return
    msg = f + " not found."
    try: 
        raise FileNotFoundError(msg)
    except:
        raise IOError(msg)

class Config(object):
    """ Read environment here to create configuration data. """

    DBSERVER   = os.environ.get('DBSERVER')
    DATABASE   = os.environ.get('DATABASE')
    DBUSER     = os.environ.get('DBUSER')
    DBPASSWORD = os.environ.get('DBPASSWORD')
       
    pass

# That's all!
