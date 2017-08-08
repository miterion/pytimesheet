import pytest

@pytest.fixture(autouse=True)
def tmpdirectory(monkeypatch):
    monkeypatch.setattr('pytimesheet.utils.get_config_path', fakeconfigpath)

def fakeconfigpath():
    return '/tmp'
