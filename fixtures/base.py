import pytest
import os


@pytest.fixture(scope='session')
def check_token():
    access_token = os.environ.get('TOKEN')
    if access_token is not None:
        return access_token
    else:
        raise Exception("There is no token. Please export valid token as an environment variable")