from simple_rest_client.api import API
from simple_rest_client.resource import Resource
import pytest
import testtools

class Repos(Resource):
    actions = {
        'list_user_repo': {'method': 'GET', 'url': 'users/{}/repos'},
        'list_public_repo': {'method': 'GET', 'url': 'repositories'},
        'create_project': {'method': 'POST', 'url': '/repos/{}/{}/projects'},
        'create_repo': {'method': 'POST', 'url': '/{}/repos' }
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

api.add_resource(resource_name='repos', resource_class=Repos)

class UsersActions(testtools.TestCase):

    def test_get_user_repos(self):
        response=api.repos.list_user_repo('SofyaTavrovskaya', body=None, params={}, headers={})
        self.assertEqual(response.status_code, 200)

    def test_create_repo(self):
        response=api.repos.create_repo('SofyaTavrovskaya', body={}, params={'name': 'test'}, headers={"Accept": "application/vnd.github.nebula-preview+json"})
        self.assertEqual(response.status_code, 201)

    def test_create_project(self):
        response=api.repos.create_project('SofyaTavrovskaya', 'test', body={"name": "test"}, params={}, headers={"Accept": "application/vnd.github.inertia-preview+json"})
        self.assertEqual(response.status_code, 201)

