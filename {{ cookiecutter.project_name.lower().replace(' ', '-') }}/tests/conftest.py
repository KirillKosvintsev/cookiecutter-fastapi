import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="function")
def auth_header():
    return '{"id":1, "external":null} '


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def api_client_authenticated(auth_header):
    client = TestClient(app)
    client.headers["X-Auth"] = auth_header
    return client


@pytest.fixture(scope="function")
def data_example_2_ids():
    return {'data': [{'header': ['sum', 'date_work'], 'id': 1390, 'name': 'Услуги ноябрь(не ноябрь)',
                      'rows': [['1786', '2019-11-01T00:00:00Z'], ['941', '2019-11-02T00:00:00Z'],
                               ['916', '2019-11-03T00:00:00Z'], ['2025', '2019-11-04T00:00:00Z']]},

                     {'header': ['sum', 'date_work'], 'id': 1557, 'name': 'Не удавшиеся звонки',
                      'rows': [['86470', '2019-11-01T00:00:00Z'], ['71076', '2019-11-02T00:00:00Z'],
                               ['50562', '2019-11-03T00:00:00Z'], ['74052', '2019-11-04T00:00:00Z']]}]}
