from flask import Blueprint, current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException, InternalServerError

from src.extensions import af

errors = Blueprint('/errors', __name__)


@errors.errorhandler(IntegrityError)
def sqlalchemy_integrity_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description
    }, error.code


@errors.errorhandler(SQLAlchemyError)
def sqlalchemy_sql_alchemy_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description
    }, error.code


@errors.errorhandler(HTTPException)
def werkzeug_http_exception(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description
    }, error.code


@errors.errorhandler(InternalServerError)
def werkzeug_internal_server_error(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description
    }, error.code


@af.error_handler()
def validation_error(code, messages): # pragma: no cover
    return {
        'code': code,
        'message': 'Validation Error',
        'description': ('The found one or more errors in the information that you sent.'),
        'errors': messages
    }, code
