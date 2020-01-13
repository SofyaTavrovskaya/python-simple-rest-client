import logging
import os
import pytest
from simple_rest_client.api import API
from simple_rest_client.resource import Resource
from fixtures.base import check_token

logger = logging.getLogger(__name__)


class Repos(Resource):
    actions = {
        'list_user_repo': {'method': 'GET', 'url': 'users/{}/repos'},
        'list_public_repo': {'method': 'GET', 'url': 'repositories'},
        'create_project': {'method': 'POST', 'url': '/repos/{}/{}/projects'},
        'create_repo': {'method': 'POST', 'url': 'user/repos'},
        'delete_repo': {'method': 'DELETE', 'url': '/repos/{}/{}'},
        'edit_repo': {'method': 'PATCH', 'url': '/repos/{}/{}'}
        }


default_params = {'access_token': os.environ.get('TOKEN')}

repos_api = API(
    api_root_url='https://api.github.com/',  # base api url
    timeout=2,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    ssl_verify=False,
    json_encode_body=True,
    params=default_params
)

repos_api.add_resource(resource_name='repos', resource_class=Repos)


@pytest.mark.repos
class TestRepos:
    def test_create_repo(self, name='test'):
        response = repos_api.repos.create_repo(body={'name': name, 'visibility': 'public'}, params={}, headers={"Accept": "application/vnd.github.nebula-preview+json", "X-OAuth-Scopes": "repo, user"})
        assert response.status_code == 201

    def test_create_repo_project(self):
        response = repos_api.repos.create_project('SofyaTavrovskaya', 'test', body={"name": "test"}, params={},
                                               headers={"Accept": "application/vnd.github.inertia-preview+json"})
        assert response.status_code == 201

    def test_delete_repo(self, name='test'):
        response = repos_api.repos.delete_repo('SofyaTavrovskaya', name, params={}, headers={"X-OAuth-Scopes":
                                                                                                "delete_repo"})
        assert response.status_code == 204

    @pytest.mark.asyncio
    @pytest.mark.repeat(3)
    async def repos_list(self):
        response = await repos_api.repos.list_user_repo('SofyaTavrovskaya', body=None, params={}, headers={})
        assert response.status_code == 200

    def test_edit_repo(self, name='test_edit'):
        self.test_create_repo(name)
        response = repos_api.repos.edit_repo('SofyaTavrovskaya', name, body={'name': 'test_edit2'}, params={},
                                             headers={"Accept": "application/vnd.github.nebula-preview+json"})
        assert response.status_code==200
        self.test_delete_repo(name='test_edit2')
