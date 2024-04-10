import os

class Config(object):
    """ Read environment here to create configuration data. """

    TEST_MODE = False
    TEST_FILE = 'lmstat.txt'
   
    _LMSTAT = '/usr/local/bin/lmstat'
    if os.path.exists(_LMSTAT):
        LMSTAT = [_LMSTAT, '-a']
    else:
        print("TEST MODE INVOKED.")
        TEST_MODE = True
    
    pass

# That's all!
