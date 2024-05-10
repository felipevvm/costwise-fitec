from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import Product, Project
from src.schemas import ProductSchema, EmptySchema

products = Blueprint('products', __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
update_product_schema = ProductSchema(partial=True)


@products.route('/products', methods=['POST'])
@authenticate(token_auth)
@body(product_schema)
@response(product_schema)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def new_product(args, project_id):
    """Create a new Product"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    product = Product(project=project, **args)
    db.session.add(product)
    db.session.commit()
    project.update_budget()
    return product


@products.route('/products', methods=['GET'])
@authenticate(token_auth)
@response(products_schema)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_products(project_id):
    """Return all Products"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return project.products


@products.route('/products/<int:product_id>', methods=['GET'])
@authenticate(token_auth)
@response(product_schema)
@other_responses({404: 'Project or Product not found', 401: 'User not allowed'})
def get_product(project_id, product_id):
    """Return a Product by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return db.session.get(Product, product_id) or abort(404)


@products.route('/products/<int:product_id>', methods=['PUT'])
@authenticate(token_auth)
@response(product_schema)
@other_responses({404: 'Project or Product not found', 401: 'User not allowed'})
def update_product(data, project_id, product_id):
    """Update a Product by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    product = db.session.get(Product, product_id) or abort(404)
    product.update(data)
    db.session.add(product)
    db.session.commit()
    project.update_budget()
    return product


@products.route('/products/<int:product_id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204, description='Product deleted')
@other_responses({404: 'Project or Product not found', 401: 'User not allowed'})
def delete_product(project_id, product_id):
    """Delete a Product by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    product = db.session.get(Product, product_id) or abort(404)
    db.session.delete(product)
    db.session.commit()
    project.update_budget()
    return {}
