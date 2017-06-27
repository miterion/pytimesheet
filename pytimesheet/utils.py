from configparser import ConfigParser
from shutil import copyfile
from os.path import expanduser, exists
import os 
from sys import platform
from subprocess import call

def get_config_path():
    return os.path.join(os.path.expanduser('~'), '.config', 'timetrack')

def get_config():
    configfile = os.path.join(get_config_path(), 'config.ini')
    if not exists(configfile):
        mk_userconfig()
    conffile = ConfigParser()
    conffile.read(configfile)
    return conffile

def mk_userconfig():
    os.makedirs(get_config_path(), exist_ok=True)
    copyfile('config.ini', path.join(configpath, 'config.ini'))

def open_file(filename):
    if platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if platform == "darwin" else "xdg-open"
        call([opener, filename])
