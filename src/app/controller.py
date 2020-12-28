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
        app.logging.info("file uploaded successfully!")
        return file_path


def analysis(file_path: str):
    """Renders template with statistical information and plots of time series
    included in file which path is given in 'file_path' argument.
    """
    try:

        # dictionary that will contains all data for rendering
        data = {}

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        file_name = os.path.split(file_path)[-1].split(".")[0]
        time_series = TimeSeries(dataset=data_file, name=file_name)
        data["analyse"] = time_series.info

        # visualisation of created time series
        plots = visualisation(file_path=file_path)
        if plots:
            data["plots"] = plots

    except Exception:
        app.logging.error(f"analysis() ERROR \n{traceback.format_exc()}")
        return render_template("500.html")
    else:
        app.logging.info(f"time series '{time_series.name}' analysis.")
        app.logging.info(time_series.info)
        return render_template("analysis.html", data=data)


def visualisation(file_path: str) -> list:
    """Creates plots of time series, that path is given as 'file_path' argument.
    This method returns list of all created and saved plots names.

    This method creates three types of plots:
    1. normal plot - that visualise time series course.
    2. autocorelation plot - visualise correlation between original and lagged time series.
    3. histogram - visualise histogram of time series values column.
    All created plots are saved to data directory.
    """
    try:

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        file_name = os.path.split(file_path)[-1].split(".")[0]
        time_series = TimeSeries(dataset=data_file, name=file_name)

        # drawing plots and saving them to files
        plots = []
        plots.append(time_series.draw())
        plots.append(time_series.draw_autocorelation(lags=100))
        plots.append(time_series.draw_histogram())

        # clearing matplotlib plot
        plt.clf()

    except Exception:
        app.logging.error(f"visualisation() ERROR \n{traceback.format_exc()}")
        return []
    else:
        app.logging.info(f"time series '{file_name}' plots created!")
        return plots


def forecast_ar(file_path: str, parameters: dict):
    """Trains and tests autoregressive model by using time series included in file,
    which path is given by 'parameters' argument, and renders forecast results.

    In first step, contents of file from given path is loaded.
    Base of loaded file content, TimeSeries class object is created.
    Before model trainin, time series is splitted to train and test subsetest
    basing on given by 'parameters' argument value.
    Train subset is used for model training, test subset, for testing model accuracy.
    After model training and test forecasting, results are plotted and saved to file.
    """
    try:

        app.logging.info("time series forecasting!")
        app.logging.info(parameters)

        # dictionary that will contains all data for rendering
        data = {}

        # preparing parameters
        data["split_ratio"] = float(parameters.get("split_ratio", 0.8))
        data["ic"] = parameters.get("ar_ic", "")

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        file_name = os.path.split(file_path)[-1].split(".")[0]
        time_series = TimeSeries(dataset=data_file, name=file_name)

        # split time series to train and test datasets
        train_data, test_data = time_series.split(ratio=data["split_ratio"])

        # creation of auto regression model
        model = AR(train_data)

        # auto regression model training
        trained_model = model.fit(ic=data["ic"])

        # forecast range
        start = len(train_data)
        end = start + len(test_data)

        # forecasting
        forecast_results = trained_model.predict(start=start, end=end)

        # plotting forecasting results and saving to file
        plt.plot(test_data, color="blue")   # plotting real values
        plt.plot(forecast_results, color='red') # plotting predicted values
        plot_name = f"{time_series.name}_forecast.png"  # name of plotted file
        plot_path = os.path.join(config.STATIC_DIR, plot_name)  # plotted file path
        plt.savefig(plot_path)  # saving plot to file

        # clearing matplotlib plot
        plt.clf()

        data["forecast_plot"] = plot_name

    except Exception:
        app.logging.error(f"time_series_forecast_ar() ERROR \n{traceback.format_exc()}")
        return render_template("500.html")
    else:
        app.logging.info(f"time series '{file_name}' forecasted successfully!")
        return render_template("ar.html", data=data)
