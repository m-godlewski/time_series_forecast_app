"""
This file contains all server errors handling.
"""


from flask import render_template

from app import APP


@APP.errorhandler(400)
def bad_request_error(error):
    return render_template("error.html", data={"error_message": "Bad Request!"})


@APP.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", data={"error_message": "Page Not Found!"})


@APP.errorhandler(405)
def method_not_allowed(error):
    return render_template("error.html", data={"error_message": "Method Not Allowed!"})


@APP.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", data={"error_message": "Internal Server Error!"})
