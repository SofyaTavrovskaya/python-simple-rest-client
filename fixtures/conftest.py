import pytest
import os


@pytest.fixture(scope='function')
def check_token():
    if os.environ.get('TOKEN') is not None:
        return 0
    else:
        raise Exception("There is not token. Please export valid token as environment variable")

