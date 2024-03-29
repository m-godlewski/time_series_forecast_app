"""
Contoller file.

This file contains all methods that are called by route.py file.
"""


import os
import traceback

from flask import render_template
from math import sqrt
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA

import app
import config
from app.utills.file_manager import FileManager
from app.models.time_series import TimeSeries


def home_page():
    """Renders home page, the 'index.html' template."""
    return render_template("index.html")


def analysis(file_path: str):
    """Renders template with statistical information and plots of time series
    included in file, which path is given by 'file_path' argument.
    """
    try:

        # dictionary that will contain all data for rendering
        data = {}

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        name = FileManager.get_file_name_from_(path=file_path)
        time_series = TimeSeries(dataset=data_file, name=name)
        data["analyse"] = time_series.info

        # visualisation of created time series
        plots = _visualisation(file_path=file_path)
        if plots:
            data["plots"] = plots

    except Exception:
        app.logging.error(f"analysis() -> \n{traceback.format_exc()}")
    else:
        app.logging.info(f"time series '{time_series.name}' analysis.")
        app.logging.info(time_series.info)
        return render_template("analysis.html", data=data)


def forecast_ar(file_path: str, parameters: dict):
    """Trains and tests autoregressive model by using time series included in file,
    which path is given by 'file_path' argument, and renders forecast results.

    In first step, contents of file from given path is loaded.
    Base of loaded file content, TimeSeries class object is created.
    Before model training, time series is splitted to train and test subsetest
    basing on given by 'parameters' argument value.
    Training subset is used for model training, test subset, for testing model accuracy.
    Model is trained base on received from HTML form parameters.
    After model training and test forecasting, results are plotted and saved to file.
    At the end, this method renders template with forecast results plot, and its parameters.
    """
    try:

        app.logging.info("time series forecasting using AR")
        app.logging.info(f"parameters = {parameters}")

        # dictionary that will contain all data for rendering
        data = {}

        # preparing parameters
        data["split_ratio"] = float(parameters.get("split_ratio", 0.8))
        data["ic"] = parameters.get("ar_ic", "")

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        name = FileManager.get_file_name_from_(path=file_path)
        time_series = TimeSeries(dataset=data_file, name=name)

        # split time series to train and test datasets
        train_data, test_data = time_series.split(ratio=data["split_ratio"])

        # creation of auto regression model
        model = AR(train_data)

        # auto regression model training
        trained_model = model.fit(ic=data["ic"])

        # forecast range
        start = len(train_data)
        end = start + len(test_data) - 1

        # forecasting
        forecast_results = trained_model.predict(start=start, end=end)

        # RMSE - root-mean-square error
        rmse = sqrt(mean_squared_error(test_data, forecast_results))

        # plotting forecasting results and saving to file
        plt.plot(test_data, color="blue", label="rzeczywiste")   # plotting real values
        plt.plot(forecast_results, color="red", label="prognozowane") # plotting predicted values
        plt.legend(loc="upper right")
        plot_name = f"{time_series.name}_forecast_ar_{data['ic']}_{data['split_ratio']}.png"  # name of plotted file
        plot_path = os.path.join(config.STATIC_DIR, plot_name)  # plotted file path
        plt.savefig(plot_path)  # saving plot to file

        # clearing matplotlib plot
        plt.clf()

        # preparing data for template rendering
        data["forecast_plot"] = plot_name
        data["lag"] = trained_model.k_ar
        data["tobs"] = trained_model.n_totobs
        data["rmse"] = rmse
        data["ic"] = config.IC_METHODS[data["ic"]]

    except Exception:
        app.logging.error(f"forecast_ar() -> {traceback.format_exc()}")
    else:
        app.logging.info(f"time series '{name}' forecasted successfully using AR!")
        return render_template("ar.html", data=data)


def forecast_arima(file_path: str, parameters: dict):
    """Trains and tests ARIMA model by using time series included in file,
    which path is given by 'file_path' argument, and renders forecast results.

    In first step, contents of file from given path is loaded.
    Base of loaded file content, TimeSeries class object is created.
    Before model training, time series is splitted to train and test subsetest
    basing on given by 'parameters' argument value.
    Training subset is used for model training, test subset, for testing model accuracy.
    Model is trained base on received from HTML form parameters.
    After model training and test forecasting, results are plotted and saved to file.
    At the end, this method renders template with forecast results plot, and its parameters.
    """
    try:

        app.logging.info("time series forecasting using ARIMA")
        app.logging.info(parameters)

        # dictionary that will contain all data for rendering
        data = {}

        # preparing parameters
        data["split_ratio"] = float(parameters.get("split_ratio", 0.8))
        data["ar"] = int(parameters.get("arima_ar", 10))
        data["i"] = int(parameters.get("arima_i", 1))
        data["ma"] = int(parameters.get("arima_ma", 2))

        # loads content of file
        data_file = FileManager.read_file(file_name=file_path)

        # creation of TimeSeries object
        name = FileManager.get_file_name_from_(path=file_path)
        time_series = TimeSeries(dataset=data_file, name=name)

        # split time series to train and test datasets
        train_data, test_data = time_series.split(ratio=data["split_ratio"])

        # creation of ARIMA model
        model = ARIMA(
            train_data,
            order = (
                data["ar"],
                data["i"],
                data["ma"]
            )
        )

        # ARIMA model training
        trained_model = model.fit()

        # forecast range
        steps = len(test_data)

        # forecasting
        forecast_results = trained_model.forecast(steps=steps)[0]

        # plotting forecasting results and saving to file
        plt.plot(test_data, color="blue", label="rzeczywiste")   # plotting real values
        plt.plot(forecast_results, color="red", label="prognozowane") # plotting predicted values
        plt.legend(loc="upper right")
        plot_name = f"{time_series.name}_forecast_arima_{data['ar']}_{data['i']}_{data['ma']}.png"  # name of plotted file
        plot_path = os.path.join(config.STATIC_DIR, plot_name)  # plotted file path
        plt.savefig(plot_path)  # saving plot to file

        # clearing matplotlib plot
        plt.clf()

        # preparing data for template rendering
        data["forecast_plot"] = plot_name
        data["tobs"] = trained_model.n_totobs
        data["aic"] = trained_model.aic
        data["bic"] = trained_model.bic
        data["hqic"] = trained_model.hqic

    except Exception:
        app.logging.error(f"forecast_arima() -> {traceback.format_exc()}")
    else:
        app.logging.info(f"time series '{name}' forecasted successfully using ARIMA!")
        return render_template("arima.html", data=data)


def _visualisation(file_path: str) -> list:
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
        app.logging.error(f"visualisation() -> {traceback.format_exc()}")
        return []
    else:
        app.logging.info(f"time series '{file_name}' plots created!")
        return plots
