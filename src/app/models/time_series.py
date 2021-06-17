import os
import traceback
from typing import Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf

import app
import config


class TimeSeries:
    """Python class representation of time series.

    Objects of this class contains analytical data properties, like:
    - minimum value
    - maximum value
    - average value
    - standard deviation value
    - interquartile value
    Each object contains also public methods that returns selected quantile of time series or list of distans points.
    This class also contains processing methods like splittinng time series values to two subsets or time series differencing.
    Values of this TimeSeries object can be visualised by methods like: draw, draw_autocorelation and draw_histogram.
    """

    def __init__(self, dataset: pd.DataFrame, name: str) -> object:
        """Constructor, that creates TimeSeries object.
        
        Before object creation, given dataset is validated for data type correction.
        After successful validation, dataset missing values ​​are completed and numerical values ​​are standardized.
        """
        try:

            # data type validation
            if self._data_type_validation(dataset=dataset):
                self.name = name
                self.data = self._data_complement(dataset=dataset)
                self.data = self._data_unification(dataset=dataset)
            else:
                app.logging.error("Given dataset data types are incorrect!")
                raise TypeError

        except Exception:
            app.logging.error(f"TimeSeries.__init__() -> {traceback.format_exc()}")

    def __str__(self) -> str:
        """Returns string representation of time series"""
        return(self.data.to_string())

    # region PROPERTIES

    @property
    def info(self) -> dict:
        """Returns all properties of TimeSeries object."""
        return {
            "minimum_value": self.min_value,
            "maximum_value": self.max_value,
            "average_value": self.average_value,
            "median_value": self.median_value,
            "standard_deviation_value": self.std_deviation_value,
            "interquartile_value": self.interquartile_value,
        }

    @property
    def min_value(self) -> float:
        """Returns minimum value of time series."""
        return self.data["value"].min().round(2)

    @property
    def max_value(self) -> float:
        """Returns maximum value of time series."""
        return self.data["value"].max().round(2)

    @property
    def average_value(self) -> float:
        """Returns average value of time series."""
        return self.data["value"].mean().round(2)

    @property
    def median_value(self) -> float:
        """Returns median value of time series."""
        return self.data["value"].median().round(2)

    @property
    def std_deviation_value(self) -> float:
        """Returns standard deviation value of time series."""
        return self.data["value"].std().round(2)

    @property
    def interquartile_value(self) -> float:
        """Returns interquartile value of time series.
        Interquantile is difference between third and first quartile.
        """
        return stats.iqr(self.data["value"], interpolation="midpoint").round(2)

    # endregion
 
    # region PUBLIC METHODS

    def get_quantile(self, q: int) -> float:
        """Returns given by 'q' argument quantile of time series dataset 'value' column."""
        return self.data["value"].quantile(q=q)

    def get_distant_points(self) -> np.array:
        """Returns numpy array of distant points.
        Distant points are values lower than Q1 - 1.5 * IQ or higher than Q3 + 1.5 * IQ.
        IQ means interquartile, Q1 and Q3 means first and thrid quartile.
        """

        # calculation of upper and lower border
        q1 = self.get_quantile(q=0.25) - 1.5 * self.interquartile_value
        q3 = self.get_quantile(q=0.75) + 1.5 * self.interquartile_value

        # values lower than lower border
        lower = self.data.loc[self.data["value"] < q1]
        lower = lower["value"].values

        # values higher than upper border
        higher = self.data.loc[self.data["value"] > q3]
        higher = higher["value"].values

        # concating two numpy arrays
        distant_points = np.concatenate((lower, higher), axis=0)

        return distant_points

    def split(self, ratio: float) -> Union[list, list]:
        """Splits time series values to two subsets,
        base on value given as 'ratio' argument and returns both as lists."""
        # size of time series
        time_series_size = len(self.data)
        # threshold of division
        threshold = int(ratio * time_series_size)
        # training and test subsets
        train_dataset = self.data["value"][:threshold].values
        test_dataset = self.data["value"][threshold:].values
        return train_dataset, test_dataset 

    def difference(self, p: int):
        """Makes time series differencing with number of periods defined by 'p' argument."""
        self.data["value"] = self.data["value"].diff(periods=p)
        self.data = self.data[1:]

    # endregion

    # region VISUALISATION METHODS

    def draw(self) -> str:
        """Plot time series graph and save created graph to file.
        Returns saved figure file name.
        """
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # polting time series with legends and labels
            plot_dataset.plot(rot=15, legend=False, xlabel="Data", ylabel="Wartość")

            # seting layout of figure
            plt.tight_layout()

            # figure file name and file path
            file_name = f"{self.name}_plot.png"
            path = os.path.join(config.STATIC_DIR, file_name)

        except Exception:
            app.logging.error(f"TimeSeries.draw() -> {traceback.format_exc()}")
        else:
            # saving figure to file
            plt.savefig(path, format="png", dpi=200)
            return file_name

    def draw_histogram(self) -> str:
        """Plot time series histogram and save created graph to file.
        Returns saved figure file name.
        """
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # ploting dataset histogram
            plot_dataset.hist()

            # figure file name and file path
            file_name = f"{self.name}_histogram.png"
            path = os.path.join(config.STATIC_DIR, file_name)

        except Exception:
            app.logging.error(f"TimeSeries.draw_histogram() -> {traceback.format_exc()}")
        else:
            # saving figure to file
            plt.savefig(path, format="png", dpi=200)
            return file_name

    def draw_autocorelation(self, lags: int) -> str:
        """Plot autocorelation function of time series for given as 'lags' argument lag value.
        Returns saved figure file name.
        """
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # ploting autocorelation function
            plot_acf(plot_dataset, lags=lags, title="Autokorelacja")

            # figure file name and file path
            file_name = f"{self.name}_autocorelation_{lags}.png"
            path = os.path.join(config.STATIC_DIR, file_name)

        except Exception:
            app.logging.error(f"TimeSeries.draw_autocorelation() -> {traceback.format_exc()}")
        else:
            # saving figure to file
            plt.savefig(path, format="png", dpi=200)
            return file_name

    # endregion

    # region PRIVATE METHODS
    
    def _data_type_validation(self, dataset: pd.DataFrame) -> bool:
        """Checks if dataset has correct datatypes in columns and if all values are positive.
        Returns validation result as boolean value.
        """
        # checking types of data in columns
        if (dataset["date"].dtype == np.object) and (dataset["value"].dtype == np.float64):
            # checking if all values in 'value' column are higher than zero
            if dataset["value"].gt(0).all():
                return True
        else:
            return False
    
    def _data_complement(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Checks complementation of dataset and return corrected dataset.
        If 'data' column value is missing, removes this row.
        If 'value' column value is NaN or zero, replace this value by average value of neighbour values.
        """
        # checks if any value in 'date' column has no value
        # if it is, drop this row
        if dataset["date"].isnull().any():
            dataset.dropna(subset=["date"], inplace=True)

        # checks if any value in 'value' column is NaN or has zero value
        # if it is, replace this value by average value of neighbour values
        if dataset["value"].isnull().any() or (dataset["value"] == 0).any():
            dataset.replace(to_replace=0, value=np.nan, inplace=True)
            dataset.interpolate(inplace=True)

        return dataset

    def _data_unification(sefl, dataset: pd.DataFrame) -> pd.DataFrame:
        """Unify 'value' column values of given dataset, by rounding all of values to one decimal place."""
        dataset = dataset.round(1)
        return dataset

    # endregion
