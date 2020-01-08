import pytest
from token_example import TOKEN
from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class Users(Resource):
    actions = {
        'authorization': {'method': 'GET', 'url': ''},
        'list': {'method': 'GET', 'url': 'users'},
        'profile': {'method': 'GET', 'url': 'users/{}'},
        'info': {'method': 'GET', 'url': 'users/{}/hovercard'},
        }


default_params = {'access_token': TOKEN}


user_api = API(
    api_root_url='https://api.github.com/',  # base api url
    timeout=2,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    ssl_verify=False,
    json_encode_body=True,
    params=default_params
)

user_api.add_resource(resource_name='users', resource_class=Users)


@pytest.mark.repeat(3)
@pytest.mark.users
def test_authorization():
    response = user_api.users.authorization(body=None, params={}, headers={'token': TOKEN})
    assert response.status_code == 200


@pytest.mark.users
def test_get_user_profile():
    response = user_api.users.profile('SofyaTavrovskaya', body=None, params={}, headers={})
    assert response.status_code == 200


@pytest.mark.users
def test_get_user_info():
    response = user_api.users.info('octicon', body=None, params={}, headers={})
    assert response.status_code == 200


@pytest.mark.users
def test_user_list():
    response = user_api.users.list(body=None, params={}, headers={})
    assert response.status_code == 200
