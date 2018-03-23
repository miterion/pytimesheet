from configparser import ConfigParser
from shutil import copyfile
from os.path import exists, join
import os
from sys import platform
from subprocess import call
from pathlib import Path
from pkg_resources import Requirement, resource_filename

def get_config_path():
    return os.path.join(os.path.expanduser('~'), '.config', 'pytimesheet')


def get_config():
    configfile = os.path.join(get_config_path(), 'config.ini')
    if not exists(configfile):
        mk_userconfig()
    conffile = ConfigParser()
    conffile.read(configfile)
    return conffile


def mk_userconfig():
    configpath = get_config_path()
    os.makedirs(configpath, exist_ok=True)
    template_config = resource_filename('pytimesheet', 'config.ini')
    copyfile(template_config, os.path.join(configpath, 'config.ini'))


def open_file(filename):
    if platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if platform == "darwin" else "xdg-open"
        call([opener, filename])


def get_path(filecontent):
    return Path(filecontent).parent
