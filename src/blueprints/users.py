from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import User
from src.schemas import AllUsersSchema, UserSchema, EmptySchema

users = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = AllUsersSchema(many=True)
update_user_schema = UserSchema(partial=True)


@users.route('/users', methods=['GET'])
@response(users_schema)
def get_users():
    """Shows all Users"""
    return User.query.all()


@users.route('/users', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
def new_user(args):
    """Create a new User"""
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@users.route('/users/<int:user_id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_user(user_id):
    """Return a User by id"""
    return db.session.get(User, user_id) or abort(404)


@users.route('/users', methods=['PUT'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
@other_responses({404: 'User not found'})
def update_user(data):
    """Update User data"""
    user = token_auth.current_user() or abort(404)
    user.update(data)
    db.session.commit()
    return user


@users.route('/users', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204, description='User deleted')
@other_responses({404: 'User not found'})
def delete_user():
    """Delete a User"""
    user = token_auth.current_user() or abort(404)
    db.session.delete(user)
    db.session.commit()
    return {}
