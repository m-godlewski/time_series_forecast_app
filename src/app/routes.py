"""
Main routing file.

This file handling all request to general endpoint.
"""


from flask import jsonify

from app import APP


@APP.route("/")
@APP.route("/index", methods=["GET"])
def index():
    return jsonify("timeseries prediction app"), 200
