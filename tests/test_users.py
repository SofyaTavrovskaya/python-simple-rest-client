import logging
import os
import pytest
from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from fixtures.base import check_token


logger = logging.getLogger(__name__)


class Users(Resource):
    actions = {
        'authorization': {'method': 'GET', 'url': ''},
        'list': {'method': 'GET', 'url': 'users'},
        'profile': {'method': 'GET', 'url': 'users/{}'},
        'info': {'method': 'GET', 'url': 'users/{}/hovercard'},
        }


default_params = {'access_token': os.environ.get('TOKEN')}


user_api = API(
    api_root_url='https://api.github.com/',  # base api url
    timeout=2,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    ssl_verify=False,
    json_encode_body=True,
    params=default_params
)

user_api.add_resource(resource_name='users', resource_class=Users)


@pytest.mark.users
class TestUsers:
    def test_authorization(self):
        response = user_api.users.authorization(body=None, params={}, headers={'token': os.environ.get('TOKEN')})
        assert response.status_code == 200

    def test_get_user_profile(self):
        response = user_api.users.profile('SofyaTavrovskaya', body=None, params={}, headers={})
        assert response.status_code == 200

    def test_get_user_info(self):
        response = user_api.users.info('SofyaTavrovskaya', body=None, params={}, headers={})
        assert response.status_code == 200

    def test_user_list(self):
        response = user_api.users.list(body=None, params={}, headers={})
        assert response.status_code == 200
