from os.path import isfile

import pytimesheet.utils 

class TestUtils:

    def test_mkuserconfig(self, monkeypatch, fakeconfigpath):
        pytimesheet.utils.mk_userconfig() 
        assert isfile(fakeconfigpath() + '/config.ini')

    def test_get_config(self):
        pytimesheet.utils.get_config()
