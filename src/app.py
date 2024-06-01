import warnings

from flask import Flask, redirect

from .extensions import db, ma, af, mail, cors

URL_PREFIX = '/api/v1/'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Config
    app.config.from_object('config')

    if test_config is not None:
        app.config.from_mapping(test_config)

    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name ",
    )

    # Extensions
    db.init_app(app)
    ma.init_app(app)
    af.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    # Blueprints
    from .blueprints.errors import errors
    app.register_blueprint(errors)
    from .blueprints.users import users
    app.register_blueprint(users, url_prefix=URL_PREFIX)
    from .blueprints.tokens import tokens
    app.register_blueprint(tokens, url_prefix=URL_PREFIX)
    from .blueprints.projects import projects
    app.register_blueprint(projects, url_prefix=URL_PREFIX)

    @app.route('/')
    def index():  # pragma: no cover
        return redirect('/docs')

    return app
