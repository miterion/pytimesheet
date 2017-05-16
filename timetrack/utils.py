from configparser import ConfigParser

def get_config():
    conffile = ConfigParser()
    conffile.read('../config.ini')
    return conffile
