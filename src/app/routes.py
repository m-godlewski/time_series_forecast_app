"""
Main routing file.

This file handling all request to general endpoint.
"""


from flask import jsonify
from flask import render_template
from flask import request

from app import APP
from app import controller


@APP.route("/")
@APP.route("/index", methods=["GET"])
def index():
    """Returns home/index response."""
    return jsonify(
        {
            "data": {},
            "info": "Time Series Forecast APP",
            "success": True
        }
    )


@APP.route("/analysis", methods=["POST"])
def analysis():
    """This route calls method that analyse time series stored in file.

    Currently supported file formats are: *.csv.
    Body of this request should have following structure:
    {
        "file_name" - <str> - name of file to analyse.
    }
    """
    return controller.time_series_analysis(parameters=request.get_json())


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