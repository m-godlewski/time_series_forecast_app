"""
Main routing file.

This file handling all request to general endpoint.
"""


from flask import redirect
from flask import request
from flask import session
from flask import url_for

from app import APP
from app import controller


@APP.route("/", methods=["GET"])
def home():
    """This route calls method, that renders home page of APP."""
    return controller.home_page()


@APP.route("/upload", methods=["POST"])
def upload():
    """This route is called by file uploading form at home page.
    After successful file uploading, this method redirects to 'analysis' endpoint.
    """
    # calling upload file method, that returns absolute path to uploaded file
    file_path = controller.upload_file(request=request)

    # adding 'file_path' to sesssion variables
    session["file_path"] = file_path

    # redirection to analysis endpoints
    return redirect(url_for("analysis"), code=307)


@APP.route("/analysis", methods=["POST"])
def analysis():
    """This route calls method that analyse and visualise time series stored in file."""
    # retrieving path to file from session
    file_path = session["file_path"]

    # calling analysis method
    return controller.time_series_analysis(file_path=file_path)


@APP.route("/visualisation", methods=["POST"])
def visualisation():
    """This route calls method, that visualise time series stored in file.

    Currently supported file formats are: *.csv.
    Body of this request should have following structure:
    {
        "file_name" - <str> - name of file to analyse.
    }
    """
    return controller.time_series_visualisation(parameters=request.get_json())


@APP.route("/forecast/ar", methods=["POST"])
def forecast_ar():
    """This route calls method that forecast future value of time series
    stored in file, by using auto regression model.

    Currently supported file formats are: *.csv.
    Body of this request should have following structure:
    {
        "file_name" - <str> - name of file to analyse.
        "split_raio" - <float> - ratio of train/test dataset split.
    }
    """
    return controller.time_series_forecast_ar(parameters=request.get_json())


@APP.route("/forecast/arima", methods=["POST"])
def forecast_arima():
    """"""
    return controller.time_series_forecast_arima()