from pathlib import Path
import pytest

@pytest.fixture(autouse=True)
def tmpdirectory(monkeypatch, fakeconfigpath):
    monkeypatch.setattr('pytimesheet.utils.get_config_path', fakeconfigpath)
    monkeypatch.setattr('pytimesheet.storage.get_config_path', fakeconfigpath)

@pytest.fixture(scope='session')
def fakeconfigpath(tmpdir_factory):
    return lambda : str(tmpdir_factory.getbasetemp())

