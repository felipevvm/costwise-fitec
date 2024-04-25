from flask import Blueprint, abort, jsonify
from apifairy import response, body, other_responses

from .models import User, db
from .schemas import UserSchema, EmptySchema

users = Blueprint('users', __name__)

user_schema = UserSchema()
update_user_schema = UserSchema(partial=True)
users_schema = UserSchema(many=True)


@users.route('/users', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
def new_user(args):
    """Create a new User"""
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@users.route('/users', methods=['GET'])
@response(users_schema)
def all_users():
    """Shows all users"""
    return User.query.all()
    # all_users_query = User.query.all()
    # result = users_schema.dump(all_users_query)
    # return jsonify(result)


@users.route('/users/<int:user_id>', methods=['GET'])
@response(user_schema)
@other_responses({404: 'User not found'})
def get_user(user_id):
    """Return a user by id"""
    return db.session.get(User, user_id) or abort(404)


@users.route('/users/<int:user_id>', methods=['PUT'])
@body(update_user_schema)
@response(user_schema)
@other_responses({404: 'User not found'})
def update_user(data, user_id):
    """Update user data"""
    user = db.session.get(User, user_id) or abort(404)
    user.update(data)
    db.session.commit()
    return user


@users.route('/users/<int:user_id>', methods=['DELETE'])
@response(EmptySchema, 204, description='User deleted')
@other_responses({404: 'User not found'})
def delete_user(user_id):
    """Delete a user by id"""
    user = db.session.get(User, user_id) or abort(404)
    db.session.delete(user)
    db.session.commit()
    return {}
