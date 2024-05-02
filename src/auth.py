from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from .extensions import db
from .models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    if username and password:
        user = db.session.scalar(User.query.filter_by(username=username))
        if user and user.verify_password(password):
            return user


@token_auth.verify_token
def verify_token(access_token):
    if access_token:
        return User.verify_access_token(access_token)
