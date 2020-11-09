"""
Main routing file.

This file handling all request to general endpoint.
"""


from flask import jsonify
from flask import render_template

from app import APP


@APP.route("/")
@APP.route("/index", methods=["GET"])
def index():
    return render_template("index.html")