from os.path import isdir
import pytest

import pytimesheet.storage

class TestStorage:
    def test_newjobfolder(self, fakeconfigpath):
        pytimesheet.storage.newjobfolder()
        assert isdir(fakeconfigpath() + '/job')


    @pytest.mark.parametrize('inputs', ['newjob1', 'newjob2'])
    def test_newjob(self, fakeconfigpath, inputs):
        pytimesheet.storage.newjob(inputs)
        assert isdir(fakeconfigpath() + '/job/' + inputs)

    
    @pytest.mark.parametrize('inputs', ['newmonth1', 'newmonth2', 'newjob1'])
    def test_newmonth(self, fakeconfigpath, inputs):
        pytimesheet.storage.newmonth(inputs, '2')
        assert isdir(fakeconfigpath() + '/job/' + inputs + '/2/')
