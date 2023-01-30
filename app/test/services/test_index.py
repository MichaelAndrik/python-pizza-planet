import pytest


@pytest.fixture
def index_uri():
    return '/'


def test_get_index(client, index_uri):
    response = client.get(f'{index_uri}')
    print(response.data)
    pytest.assume(response.status.startswith('200'))
