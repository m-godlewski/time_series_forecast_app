"""
Main routing file.

This file handling all request to general endpoint and calls selected methods.
"""


from flask import redirect
from flask import request
from flask import session
from flask import url_for

from app import APP
from app import controller


@APP.route("/", methods=["GET"])
def home():
    """This route calls method, that renders home page of application."""
    return controller.home_page()


@APP.route("/upload", methods=["POST"])
def upload():
    """This route is called by file uploading form at home page.
    After successful file uploading, this method redirects to 'analysis' endpoint.
    """

    # calling upload file method, that uploads file to application server
    # and returns absolute path to uploaded file
    file_path = controller.upload_file(request=request)

    # adding 'file_path' to current sesssion variables
    session["file_path"] = file_path

    # redirection to analysis endpoints
    return redirect(url_for("analysis"), code=307)


@APP.route("/analysis", methods=["POST"])
def analysis():
    """This route calls method that analyse and visualise time series stored in file."""

    # retrieving path to file from session
    file_path = session["file_path"]

    # calling analysis method
    return controller.analysis(file_path=file_path)


@APP.route("/ar", methods=["POST"])
def forecast_ar():
    """This route calls method that forecast future values of time series
    stored in file, using auto regression model."""

    # retrieving path to file from session
    file_path = session["file_path"]

    # retrieving parameters from form
    parameters = {}
    for key, value in request.form.items():
        if value:
            parameters[key] = value

    # calling AR forecasting method
    return controller.forecast_ar(file_path=file_path, parameters=parameters)


@APP.route("/arima", methods=["POST"])
def forecast_arima():
    """This route calls method that forecast future values of time series
    stored in file, using ARIMA model."""

    # retrieving path to file from session
    file_path = session["file_path"]

    # retrieving parameters from form
    parameters = {}
    for key, value in request.form.items():
        if value:
            parameters[key] = value

    # calling ARIMA forecasting method
    return controller.forecast_arima(file_path=file_path, parameters=parameters)
