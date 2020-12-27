import os
import traceback
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.ar_model.AR', FutureWarning)

import numpy as np
import matplotlib.pyplot as plt
from flask import jsonify
from flask import Request
from flask import render_template
from werkzeug.utils import secure_filename
from statsmodels.tsa.ar_model import AR

import app
import config
from app.models.time_series import TimeSeries
from app.utills.file_manager import FileManager


def home_page():
    """Renders home page."""
    return render_template("index.html")


def upload_file(request: Request) -> str:
    """Uploads file received by request, saves it and returns absolute path to this file."""
    try:

        # retrieves file from request
        f = request.files["file"]

        # absoulte path to file
        file_path = os.path.join(config.DATA_DIR, secure_filename(f.filename))

        # saves received file
        f.save(file_path)

    except Exception:
        app.logging.error(f"upload_file() ERROR \n{traceback.format_exc()}")
        return ""
    else:
        app.logging.info("File uploaded successfully!")
        return file_path


def time_series_analysis(file_path: str):
    """Returns statistical information of time series included in file 
    which path is given in 'parameters' variable.
    
    Returned response contains information like:
    - average value
    - interquartile value
    - maximum value
    - minimum value
    - standard deviation value
    """
    try:

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        time_series = TimeSeries(dataset=data_file, name="test")

    except Exception:
        app.logging.error(f"time_series_analysis() ERROR \n{traceback.format_exc()}")
        return jsonify({
                "data": {},
                "info": "time series analysis error!",
                "success": False
            }), 200
    else:
        app.logging.info(f"'{time_series.name}' time series analysis.")
        app.logging.info(time_series.info)
        return render_template("analysis.html", data=time_series.info)


def time_series_visualisation(parameters: dict):
    """Plots time series included in file which path is given in 'parameters' argument.j

    This method creates three types of plots:
    1. normal plot - that visualise time series course.
    2. autocorelation plot - visualise correlation between original and lagged time series.
    3. histogram - visualise histogram of time series values column.
    """
    try:

        # checks if there is 'file_name' field in received dictionary
        if not "file_name" in parameters:
            app.logging.error("parameter 'file_name' is missing")
            return jsonify({
                    "data": {},
                    "info": "parameter 'file_name' is missing"
                }), 400
        else:
            file_name = parameters.get("file_name")

        # loads content of file
        data_file = FileManager.read_file(file_name=file_name)

        # creation of TimeSeries object
        name = file_name.split(".")[0]
        time_series = TimeSeries(dataset=data_file, name=name)

        # drawing plots and saving them to files
        time_series.draw()
        time_series.draw_autocorelation(lags=100)
        time_series.draw_histogram()

        # clearing matplotlib plot
        plt.clf()

    except Exception:
        app.logging.error(f"time_series_visualisation() ERROR \n{traceback.format_exc()}")
        return jsonify({
                "data": {},
                "info": "time series visualisation error!",
                "success": False
            }), 200
    else:
        app.logging.info("")
        return jsonify({
                "data": {},
                "info": "",
                "success": True
            }), 200


def time_series_forecast_ar(parameters: dict):
    """Trains and tests autoregressive model by using time series included in file,
    which path is given by 'parameters' argument.

    In first step, contents of file from given path is loaded.
    Base of loaded file content, TimeSeries class object is created.
    Before model trainin, time series is splitted to train and test subsetest
    basing on given by 'parameters' argument value.
    Train subset is used for model training, test subset, for testing model accuracy.
    After model training and test forecasting, results are plotted and saved to file.
    """
    try:

        # checks if there is 'file_name' field in received dictionary
        if not "file_name" in parameters:
            app.logging.error("parameter 'file_name' is missing")
            return jsonify({
                    "data": {},
                    "info": "parameter 'file_name' is missing"
                }), 400

        file_name = parameters.get("file_name")
        ratio = parameters.get("split_ratio", 0.8)

        # loads content of file
        data_file = FileManager.read_file(file_name=file_name)

        # creation of TimeSeries object
        name = file_name.split(".")[0]
        time_series = TimeSeries(dataset=data_file, name=name)

        # split time series to train and test datasets
        train_data, test_data = time_series.split(ratio=ratio)

        # creation of auto regression model
        model = AR(train_data)

        # auto regression model training
        trained_model = model.fit()

        # forecast range
        start = len(train_data)
        end = start + len(test_data)

        # forecasting
        forecast_results = trained_model.predict(start=start, end=end)

        # plotting forecasting results and saving to file
        plt.plot(test_data, color="blue")
        plt.plot(forecast_results, color='red')
        plt.savefig(f"{config.RESULTS_DIR}/{time_series.name}_forecast.png")

    except Exception:
        app.logging.error(f"time_series_forecast_ar() ERROR \n{traceback.format_exc()}")
        return jsonify({
                "data": {},
                "info": "time series AR forecast error!",
                "success": False
            }), 200
    else:
        app.logging.info("")
        return jsonify({
                "data": forecast_results.tolist(),
                "info": "",
                "success": True
            }), 200


def time_series_forecast_arima():
    """"""
    try:
        pass
    except Exception:
        app.logging.error(f"time_series_forecast_arima() ERROR \n{traceback.format_exc()}")
        return jsonify({
                "data": {},
                "info": "time series ARIMA forecast error!",
                "success": False
            }), 200
    else:
        app.logging.info("")
        return jsonify({
                "data": {},
                "info": "",
                "success": True
            }), 200