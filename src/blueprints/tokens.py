from flask import Blueprint, abort, current_app, request, url_for
from apifairy import authenticate, response, other_responses, body
from werkzeug.http import dump_cookie

from src.extensions import db
from src.auth import basic_auth, token_auth
from src.models import User, Token
from src.schemas import TokenSchema, PasswordResetRequestSchema, PasswordResetSchema, EmptySchema
from src.email import send_email

tokens = Blueprint('tokens', __name__)
token_schema = TokenSchema()
request_reset_schema = PasswordResetRequestSchema()
reset_schema = PasswordResetSchema()


def token_response(token):
    headers = {}
    if current_app.config['REFRESH_TOKEN_IN_COOKIE']:
        headers['Set-Cookie'] = dump_cookie(
            'refresh_token',
            token.refresh_token,
            path=url_for('tokens.new_tokens'),
            secure=not current_app.config['DEBUG'],
            httponly=not current_app.config['DEBUG'],
        )
    return {
        'access_token': token.access_token_jwt,
        'refresh_token': token.refresh_token if current_app.config['REFRESH_TOKEN_IN_BODY'] else None
    }, 200, headers


@tokens.route('/tokens', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
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
    refresh_token = args.get('refresh_token', request.cookies.get('refresh_token'))
    if not access_token_jwt or not refresh_token:
        abort(401)
    token = User.verify_refresh_token(refresh_token, access_token_jwt)
    if not token:
        abort(401)
    token.expire()
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


@tokens.route('/tokens/reset', methods=['POST'])
@body(PasswordResetRequestSchema)
@response(EmptySchema, status_code=204, description='Password reset email sent')
@other_responses({404: 'User not found'})
def request_reset(args):
    """Request a password reset token"""
    user = db.session.query(User).filter_by(email=args['email']).scalar() or abort(404)
    if user is not None:
        reset_token = user.generate_reset_token()
        reset_url = current_app.config['PASSWORD_RESET_URL'] + f'?token={reset_token}'
        send_email(args['email'], user.username, reset_url)
    return {}


@tokens.route('/tokens/reset', methods=['PUT'])
@body(PasswordResetSchema)
@response(EmptySchema, status_code=204, description='Password reset successful')
@other_responses({400: 'Invalid reset token'})
def password_reset(args):
    """Reset a user password"""
    user = User.verify_reset_token(args['token']) or abort(400)
    user.password = args['new_password']
    db.session.commit()
    return {}
