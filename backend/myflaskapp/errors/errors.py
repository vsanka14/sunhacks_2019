from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
import sys

def error_response(status_code, message, traceback):
    payload = {
        'code': status_code,
        'message': message,
        'traceback': traceback
    }
    return jsonify(payload)

def bad_request(msg):
    template = "A HTTP exception of type {0} occured. {1}"
    message = template.format(HTTP_STATUS_CODES.get(400), msg)
    return error_response(400, message, None)
