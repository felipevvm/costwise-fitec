from flask import Blueprint, abort, current_app, request
from apifairy import authenticate, response, other_responses, body

from src.extensions import db
from src.auth import basic_auth, token_auth
from src.models import User, Token
from src.schemas import TokenSchema, EmptySchema

tokens = Blueprint('tokens', __name__)
token_schema = TokenSchema()


def token_response(token):
    return {
        'access_token': token.access_token_jwt,
        'refresh_token': token.refresh_token if current_app.config['REFRESH_TOKEN_IN_BODY'] else None
    }, 200


@tokens.route('/tokens', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid email or password'})
def new_tokens():
    """Create new Acess and Refresh tokens"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    db.session.add(token)
    token.clean()
    db.session.commit()
    return token_response(token)


@tokens.route('/tokens', methods=['PUT'])
@body(token_schema)
@response(token_schema, description='New access and refresh tokens')
@other_responses({401: 'Invalid access or refresh token'})
def refresh_access_token(args):
    """Refresh an Access token"""
    access_token_jwt = args['access_token']
    refresh_token = args.get('refresh_token')
    if not access_token_jwt or not refresh_token:
        abort(401)
    token = User.verify_refresh_token(refresh_token, access_token_jwt)
    if not token:
        abort(401)
    new_token = token.user.generate_auth_token()
    db.session.add_all([token, new_token])
    db.session.commit()
    return token_response(new_token)


@tokens.route('/tokens', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, status_code=204, description='Token revoked')
@other_responses({401: 'Invalid access token'})
def revoke_token():
    """Revoke an Access token"""
    access_token_jwt = request.headers['Authorization'].split()[1]
    token = Token.from_jwt(access_token_jwt)
    if not token:
        abort(401)
    token.expire()
    token.clean()
    db.session.commit()
    return {}
