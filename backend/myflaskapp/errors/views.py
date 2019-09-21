from flask import Blueprint, jsonify
from werkzeug import exceptions
from sqlalchemy import exc
from myflaskapp.errors.errors import error_response
from myflaskapp.extensions import db
import traceback
import sys

#global error handler for the app

blueprint = Blueprint('errors', __name__)

def handle_error(e, status_code, type_of_error):
    template = "A {0} exception of type {1} occured."
    message = template.format(type_of_error, type(e).__name__)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return error_response(status_code, message, traceback_msg)

@blueprint.app_errorhandler(500)
def handle_internal_error():
    db.session.rollback()
    status_code = 500
    message = "An internal server error occured."
    return error_response(status_code, message)

#handles all HTTP exceptions like not found, bad request, unauthorized etc
@blueprint.app_errorhandler(exceptions.HTTPException)
def handle_http_error(e):
    status_code = e.code
    return handle_error(e, status_code, 'HTTP exception')

#handles all errors relating to db with sqlchemy and postgres
@blueprint.app_errorhandler(exc.SQLAlchemyError)
def handle_sqlalchemy_error(e):
    status_code = e.code
    return handle_error(e, status_code, 'SQLAlchemy exception')


#handles all other exceptions
@blueprint.app_errorhandler(Exception)
def handle_exception_error(e):
    status_code = type(e).__name__
    return handle_error(e, status_code, None)