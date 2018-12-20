import pytest
from pidgin.app import app as pidgin_app

@pytest.fixture(scope='session')
def app():
    return pidgin_app
