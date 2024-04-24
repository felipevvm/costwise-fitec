import os

from flask import Flask
from .models import db


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

    # Database
    db.init_app(app)

    # Blueprints
    from src.users import users
    app.register_blueprint(users, url_prefix='/api')

    return app
