from src import db
from src.models import Product


def test_product_repr(database_with_data):
    """
    Given a product,
    When I call the repr method of the product object,
    Then the method should return a string with the product id, name, type and cost.
    """
    product = db.session.get(Product, 1)
    assert product is not None
    assert repr(product) == f'<Product {product.id}-{product.name_product}-{product.type}-{product.cost}>'


def test_url(database_with_data):
    """
    Given a product,
    When I call the url property of the product object,
    Then the URL should be '/api/v1/projects/<project_id>/products/<id>'.
    """
    product = db.session.get(Product, 1)
    assert product is not None
    assert product.url == f'/api/v1/projects/{product.project.id}/products/{product.id}'


def test_calc_no_license_products_total_cost(database_with_data):
    """
    Given a project with products,
    When I call the calc_no_license_products_total_cost method of the Products class,
    Then the method should return the total cost of all products with no license.
    """
    project = db.session.get(Product, 1).project
    assert project is not None

    total_cost = Product.calc_no_license_products_total_cost(project.id)
    assert total_cost == 1110


def test_calc_license_products_total_cost(database_with_data):
    """
    Given a project with products,
    When I call the calc_license_products_total_cost method of the Products class,
    Then the method should return the total cost of all products with a license.
    """
    project = db.session.get(Product, 1).project
    assert project is not None

    total_cost = Product.calc_license_products_total_cost(project.id)
    assert total_cost == 6660


def test_calc_total_costs_by_license(database_with_data):
    """
    Given a project with products,
    When I call the calc_total_costs_by_license method of the Products class,
    Then the method should return the total cost of all products by license.
    """
    project = db.session.get(Product, 1).project
    assert project is not None

    total_by_license = Product.calc_total_costs_by_license(project.id)
    assert total_by_license['no_license_cost'] == 1110
    assert total_by_license['license_cost'] == 6660


def test_calc_total_costs_by_type(database_with_data):
    """
    Given a project with products,
    When I call the calc_total_costs_by_type method of the Products class,
    Then the method should return the total cost of all products by type.
    """
    project = db.session.get(Product, 1).project
    assert project is not None

    total_by_type = Product.calc_total_costs_by_type(project.id)
    assert total_by_type['HARDWARE'] == 7000
    assert total_by_type['SOFTWARE'] == 700
    assert total_by_type['OTHER'] == 70
