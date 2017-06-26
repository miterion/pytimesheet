from configparser import ConfigParser
from shutil import copyfile
from os.path import expanduser, exists
from os import path, makedirs

def get_config_path():
    return path.join(path.expanduser('~'), '.config', 'timetrack')

def get_config():
    configfile = path.join(get_config_path(), 'config.ini')
    if not exists(configfile):
        mk_userconfig()
    conffile = ConfigParser()
    conffile.read(configfile)
    return conffile

def mk_userconfig():
    makedirs(get_config_path(), exist_ok=True)
    copyfile('config.ini', path.join(configpath, 'config.ini'))
