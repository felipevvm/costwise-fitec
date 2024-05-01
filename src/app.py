import os

from flask import Flask
from apifairy import APIFairy

from .models import db
from .schemas import ma

af = APIFairy()

URL_PREFIX = '/api/v1/'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Config
    app.config.from_object('config')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Extensions
    db.init_app(app)
    ma.init_app(app)
    af.init_app(app)

    # Blueprints
    from src.users import users
    app.register_blueprint(users, url_prefix=URL_PREFIX)
    from src.tokens import tokens
    app.register_blueprint(tokens, url_prefix=URL_PREFIX)
    return app
