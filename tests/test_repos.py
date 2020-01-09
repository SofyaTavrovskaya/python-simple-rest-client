import logging
import os
import pytest
from simple_rest_client.api import API
from simple_rest_client.resource import Resource

logger = logging.getLogger(__name__)


class Repos(Resource):
    actions = {
        'list_user_repo': {'method': 'GET', 'url': 'users/{}/repos'},
        'list_public_repo': {'method': 'GET', 'url': 'repositories'},
        'create_project': {'method': 'POST', 'url': '/repos/{}/{}/projects'},
        'create_repo': {'method': 'POST', 'url': 'user/repos'},
        'delete_repo': {'method': 'DELETE', 'url': '/repos/{}/{}'}
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


@pytest.mark.run(order=1)
@pytest.mark.repos
def test_create_repo():
    response = repos_api.repos.create_repo(body={'name': 'test', 'visibility': 'public'}, params={}, headers={"Accept": "application/vnd.github.nebula-preview+json", "X-OAuth-Scopes": "repo, user"})
    assert response.status_code == 201


@pytest.mark.run(order=2)
@pytest.mark.repos
def test_create_repo_project():
    response = repos_api.repos.create_project('SofyaTavrovskaya', 'test', body={"name": "test"}, params={}, headers={"Accept": "application/vnd.github.inertia-preview+json"})
    assert response.status_code == 201


@pytest.mark.run(order=3)
@pytest.mark.repos
def test_delete_repo():
    response = repos_api.repos.delete_repo('SofyaTavrovskaya', 'test', params={}, headers={"X-OAuth-Scopes": "delete_repo"})
    assert response.status_code == 204


@pytest.mark.repeat(10)
@pytest.mark.asyncio
@pytest.mark.repos
async def repos_list():
    response = await repos_api.repos.list_user_repo('SofyaTavrovskaya', body=None, params={}, headers={})
    assert response.status_code == 200
