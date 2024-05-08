from flask import Blueprint, current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException, InternalServerError

from src.extensions import af

errors = Blueprint('/errors', __name__)


@errors.app_errorhandler(IntegrityError)
def sqlalchemy_integrity_error(error):
    return {
        'code': 400,
        'message': 'Database error',
        'description': str(error.orig)
    }, 400


@errors.app_errorhandler(SQLAlchemyError)
def sqlalchemy_sql_alchemy_error(error):
    return {
        'code': InternalServerError.code,
        'message': InternalServerError().name,
        'description': InternalServerError.description
    }, 500


@errors.app_errorhandler(HTTPException)
def werkzeug_http_exception(error):
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description
    }, error.code


@af.error_handler
def validation_error(code, messages):
    return {
        'code': code,
        'message': 'Validation Error',
        'description': 'The found one or more errors in the information that you sent.',
        'errors': messages
    }, code
