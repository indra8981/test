import pytest
from starlette.testclient import TestClient
import json

from main import app

items = {}


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
post_url = "/post_location"
get_url = "/get_location/23.4710&88.5565"


def test_get(test_app):
    response = test_app.get(get_url)
    print(response)


def test_read_main(test_app):
    file = open("/home/indrajit1/PycharmProjects/test/TestCases/test1.json", 'r')
    request_json = json.loads(file.read())
    print(request_json)
    response = test_app.post(post_url, request_json)
    print(response)
    assert response.status_code == 400
    response = test_app.post(post_url, request_json)
    assert response.status_code == 400
