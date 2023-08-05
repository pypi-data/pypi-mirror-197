import json
import pytest
from ndclient import Client, Response

url = "https://nd.test.org"
username = "admin"
password = "password"
login_domain = "cisco"
verify = True
resource_folder = "src/tests/resources/"


@pytest.fixture()
def version_info():
    with open(resource_folder + "version.json") as f:
        return json.load(f)


@pytest.fixture()
def login_response():
    with open(resource_folder + "login.json") as f:
        return json.load(f)


@pytest.fixture()
def refresh_response():
    with open(resource_folder + "refresh.json") as f:
        return json.load(f)


@pytest.fixture()
def version_url():
    return "/appcenter/cisco/ndfc/api/v1/fm/about/version"


def test_property():
    client = Client(url, username, password, login_domain, verify)
    assert client.url == url


def test_get_version(mocker, version_url, version_info):
    resp = mocker.Mock()
    resp.json = mocker.Mock(return_value=version_info)
    resp.status_code = 200

    mocker.patch("ndclient.client.Client._send", return_value=resp)
    client = Client(url, username, password, login_domain, verify)

    version = client.send(version_url, "get")
    resp = Response()
    resp.ok = True
    resp.data = version_info
    resp.status_code = 200
    assert version == resp


def test_login(mocker, login_response):
    resp = mocker.Mock()
    resp.json = mocker.Mock(return_value=login_response)
    resp.status_code = 200

    mocker.patch("ndclient.client.Client._send", return_value=resp)
    client = Client(url, username, password, login_domain, verify)
    login = client.login()
    assert login


def test_refresh(mocker, refresh_response):
    resp = mocker.Mock()
    resp.json = mocker.Mock(return_value=login_response)
    resp.status_code = 200

    mocker.patch("ndclient.client.Client._send", return_value=resp)
    client = Client(url, username, password, login_domain, verify)
    refresh = client.refresh()
    assert refresh
