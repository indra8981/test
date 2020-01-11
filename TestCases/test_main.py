from starlette.testclient import TestClient
import json

from main import app

items = {}

client = TestClient(app)
post_url = "/post_location"
get_url = "/get_location/23.4710&88.5565"


def test_get():
    response = client.get(get_url)
    print(response)


test_get()


def test_read_main():
    file = open("/home/indrajit1/PycharmProjects/test/TestCases/test1.json", 'r')
    request_json = json.loads(file.read())
    print(request_json)
    response = client.post(post_url, request_json)
    print(response)
    assert response.status_code == 400
    response = client.post(post_url, request_json)
    assert response.status_code == 400


test_read_main()
