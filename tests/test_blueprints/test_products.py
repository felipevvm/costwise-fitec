import pytest

invalid_products_id = [0, -1, 1.5, 99999999999999]


def test_get_products(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the project products.
    """
    response = database_with_data.get('api/v1/projects/1/products', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert len(response.json) == 6
    assert response.json[0]['name_product'] == 'hardware_no_license'
    assert response.json[1]['name_product'] == 'hardware_license'
    assert response.json[2]['name_product'] == 'software_no_license'
    assert response.json[3]['name_product'] == 'software_license'
    assert response.json[4]['name_product'] == 'other_no_license'
    assert response.json[5]['name_product'] == 'other_license'


def test_new_product(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products,
    When the method is POST and the user provides valid data,
    Then the user should receive a 201 status code and the new product data.
    """
    response = database_with_data.post('api/v1/projects/1/products', json={
        'name_product': 'test_product',
        'description_product': 'test_description',
        'license': 1,
        'type': 'SOFTWARE',
        'cost': 100,
        'amount': 1,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 201
    assert response.json['id'] == 7
    assert response.json['name_product'] == 'test_product'
    assert response.json['description_product'] == 'test_description'
    assert response.json['license'] == 1
    assert response.json['type'] == 'SOFTWARE'
    assert response.json['cost'] == 100
    assert response.json['amount'] == 1
    assert response.json['project_id'] == 1


def test_get_product(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products/<product_id>,
    When the method is GET and the user provides a valid product id,
    Then the user should receive a 200 status code and the product data.
    """
    response = database_with_data.get('api/v1/projects/1/products/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_product'] == 'hardware_no_license'
    assert response.json['description_product'] == 'test_description'
    assert response.json['license'] == 0
    assert response.json['type'] == 'HARDWARE'
    assert response.json['cost'] == 1000
    assert response.json['amount'] == 1
    assert response.json['project_id'] == 1


@pytest.mark.parametrize('product_id', invalid_products_id)
def test_get_product_invalid_product_id(database_with_data, access_token_valid, product_id):
    """
    Given the protected endpoint /projects/<project_id>/products/<product_id>,
    When the method is GET and the user provides an invalid product id,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.get(f'api/v1/projects/1/products/{product_id}', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 404


def test_update_product(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products/<product_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated product data.
    """
    response = database_with_data.put('api/v1/projects/1/products/1', json={
        'name_product': 'test_product_updated',
        'description_product': 'test_description_updated',
        'license': 1,
        'type': 'SOFTWARE',
        'cost': 2000,
        'amount': 2,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_product'] == 'test_product_updated'
    assert response.json['description_product'] == 'test_description_updated'
    assert response.json['license'] == 1
    assert response.json['type'] == 'SOFTWARE'
    assert response.json['cost'] == 2000
    assert response.json['amount'] == 2
    assert response.json['project_id'] == 1


def test_update_product_invalid_data(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products/<product_id>,
    When the method is PUT and the user provides invalid data,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/projects/1/products/1', json={
        'name_product': 10.0,
        'description_product': True,
        'license': "0",
        'type': 'SOFTWARE',
        'cost': '10.0',
        'amount': 'ten',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 400


def test_delete_product(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products/<product_id>,
    When the method is DELETE and the user provides a valid product id,
    Then the user should receive a 204 status code.
    """
    response = database_with_data.delete('api/v1/projects/1/products/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 204
