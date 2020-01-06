import testtools
import imp
from simple_rest_client.api import API
from simple_rest_client.resource import Resource

class Users(Resource):
    actions = {
        'authorization': {'method': 'GET', 'url': ''},
        'list': {'method': 'GET', 'url': 'users'},
        'profile': {'method': 'GET', 'url': 'users/{}'},
        'info': {'method': 'GET', 'url': 'users/{}/hovercard'},
        }

default_params = {'access_token': 'a530cc5aceefdf2322d91cbca5c924a426b4c4e6'}

api = API(
    api_root_url='https://api.github.com/', # base api url
    timeout=2, # default timeout in seconds
    append_slash=False, # append slash to final url
    ssl_verify=False,
    json_encode_body=True,
    params=default_params
)

api.add_resource(resource_name='users', resource_class=Users)

class UsersActions(testtools.TestCase):
    def test_authorization(self):
        response=api.users.authorization(body=None, params={}, headers={'token': 'a530cc5aceefdf2322d91cbca5c924a426b4c4e6'})
        self.assertEqual(response.status_code,200)

    def test_get_user_profile(self):
        response=api.users.profile('SofyaTavrovskaya', body=None, params={}, headers={})
        self.assertEqual(response.status_code,200)

    def test_get_user_info(self):
        response=api.users.info('octicon', body=None, params={}, headers={})
        self.assertEqual(response.status_code,200) 

    def test_user_list(self):
        response=api.users.list(body=None, params={}, headers={})
        self.assertEqual(response.status_code,200)

