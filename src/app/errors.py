"""
This file contains all server errors handling.
"""


from flask import jsonify
from flask import make_response

from app import APP


@APP.errorhandler(400)
def bad_request_error(error):
    return make_response(
        jsonify({"info": "ERROR - BAD REQUEST!", "success": False}), 400
    )


@APP.errorhandler(404)
def not_found_error(error):
    return make_response(
        jsonify({"info": "ERROR - REQUEST NOT FOUND!", "success": False}), 404
    )


@APP.errorhandler(405)
def method_not_allowed(error):
    return make_response(
        jsonify({"info": "ERROR - METHOD NOT ALLOWED!", "success": False}), 405
    )


@APP.errorhandler(500)
def internal_server_error(error):
    return make_response(
        jsonify({"info": "ERROR - INTERNAL SERVER ERROR!", "success": False}), 500
    )
