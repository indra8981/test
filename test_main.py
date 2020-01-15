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
get_url = "/get_location/23949.4710&8865.5565"
get_self = "/get_using_self/28.65&77.2167&5"
get_postgre = "/get_using_postgres/28.65&77.2167&5"


def test_read_main(test_app):
    file = open("test1.json", 'r')
    request_json = json.loads(file.read())
    response = test_app.post(post_url, request_json)
    print(response.text)
    assert response.status_code == 400
    response = test_app.post(post_url, request_json)
    assert response.status_code == 400

def test_get(test_app):
    response = test_app.get(get_url)
    assert response.status_code == 404
    print(response.text)


def test_compare(test_app):
    response1 = test_app.get(get_self)
    response2 = test_app.get(get_postgre)
    print(response1.text)
    print(response2.text)
    assert response1.text == response2.text
