from flask import Blueprint, jsonify, request, abort, url_for
from apifairy import response, body, other_responses
from .models import Product, ProductType, db
from .schemas import ProductSchema, EmptySchema

products = Blueprint('products', __name__)

@products_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")

    try:
        new_product = Product(
            name_product=data['name_product'],
            cost=data['cost'],
            license=data['license'],
            type=ProductType[data['type']],  # Enum type
            amount=data.get('amount', 0),
            project_id=data['project_id']
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            'id': new_product.id,
            'name_product': new_product.name_product,
            'cost': new_product.cost,
            'license': new_product.license,
            'type': new_product.type.name,
            'amount': new_product.amount,
            'project_id': new_product.project_id,
            'url': url_for('products.get_product', id=new_product.id)
        }), 201
    except KeyError:
        abort(400, description="Missing required field")

@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name_product': p.name_product,
        'cost': p.cost,
        'license': p.license,
        'type': p.type.name,
        'amount': p.amount,
        'project_id': p.project_id,
        'url': url_for('products.get_product', id=p.id)
    } for p in products])

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        abort(404, description="Product not found")

    return jsonify({
        'id': product.id,
        'name_product': product.name_product,
        'cost': product.cost,
        'license': product.license,
        'type': product.type.name,
        'amount': product.amount,
        'project_id': product.project_id,
        'url': url_for('products.get_product', id=product.id)
    })

@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        abort(404, description="Product not found")

    data = request.get_json()
    if not data:
        abort(400, description="No data provided")

    try:
        product.name_product = data.get('name_product', product.name_product)
        product.cost = data.get('cost', product.cost)
        product.license = data.get('license', product.license)
        product.type = ProductType[data.get('type', product.type.name)]
        product.amount = data.get('amount', product.amount)

        db.session.commit()

        return jsonify({
            'id': product.id,
            'name_product': product.name_product,
            'cost': product.cost,
            'license': product.license,
            'type': product.type.name,
            'amount': product.amount,
            'project_id': product.project_id,
            'url': url_for('products.get_product', id=product.id)
        })
    except KeyError:
        abort(400, description="Invalid data field")


@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        abort(404, description="Product not found")

    db.session.delete(product)
    db.session.commit()

    return '', 204