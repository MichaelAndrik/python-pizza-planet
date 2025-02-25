import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_size_service(create_size):
    size = create_size.json
    pytest.assume(create_size.status.startswith('200'))
    pytest.assume(size['_id'])
    pytest.assume(size['name'])
    pytest.assume(size['price'])


def test_update_size_service(client, create_size, size_uri):
    current_size = create_size.json
    update_data = {
        **current_size,
        'name': get_random_string(),
        'price': get_random_price(1, 5)
    }
    response = client.put(size_uri, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_ingredient = response.json
    for param, value in update_data.items():
        pytest.assume(updated_ingredient[param] == value)


def test_get_size_by_id_service(client, create_size, size_uri):
    current_ingredient = create_size.json
    response = client.get(f'{size_uri}id/{current_ingredient["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_ingredient = response.json
    for param, value in current_ingredient.items():
        pytest.assume(returned_ingredient[param] == value)


def test_get_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith('200'))
    returned_sizes = {size['_id']: size for size in response.json}
    for ingredient in create_sizes:
        pytest.assume(ingredient['_id'] in returned_sizes)
