import traceback

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


class TimeSeries:
    """
    """

    def __init__(self, dataset: pd.DataFrame, name: str):
        """
        """
        try:

            # TODO consider flag for behaviour for missing rows
            if self._data_type_validation(dataset=dataset):
                self.name = name
                self.data = self._data_complement(dataset=dataset)
                self.data = self._data_unification(dataset=dataset)
                # TODO calculate statistical data method here
            else:
                print("given dataset datatype is incorrect")

        except Exception:
            print(f"TimeSeries.__init__() ERROR \n{traceback.format_exc()}")

    def __str__(self) -> str:
        """Returns string representation of time series"""
        return(self.data.to_string())

    # region PROPERTIES

    @property
    def min_value(self) -> float:
        """Returns minimum value of time series."""
        return self.data["value"].min()

    @property
    def max_value(self) -> float:
        """Returns maximum value of time series."""
        return self.data["value"].max()

    @property
    def average_value(self) -> float:
        """Returns average value of time series."""
        return self.data["value"].mean()

    @property
    def std_deviation_value(self) -> float:
        """Returns standard deviation value of time series."""
        return self.data["value"].std()

    @property
    def median_value(self) -> float:
        """Returns median value of time series."""
        return self.data["value"].median()

    @property
    def interquartile_value(self) -> float:
        """Returns interquartile value of time series.
        Inter quantile is difference between third and first quartile.
        """
        return stats.iqr(self.data["value"], interpolation="midpoint")

    # endregion
 
    # region PUBLIC METHODS

    def get_quantile(self, q: int) -> float:
        """Returns given by 'q' argument quantile of time series dataset 'value' column."""
        return self.data["value"].quantile(q=q)

    def get_distant_points(self) -> np.array:
        """Returns numpy array of distant points.
        Distant poinst are values lower than Q1 -1 or higher Q3 +1. 
        """

        q1 = self.get_quantile(q=0.25) - 1.5 * self.interquartile_value     # first quantile Q1 - 1.5 * interquartile
        q3 = self.get_quantile(q=0.75) + 1.5 * self.interquartile_value     # third quantile Q3 + 1.5 * interquartile

        # values lower than Q1 - 1
        lower = self.data.loc[self.data["value"] < q1]
        lower = lower["value"].values

        # values higher than Q3 + 1
        higher = self.data.loc[self.data["value"] > q3]
        higher = higher["value"].values

        # concating two numpy arrays
        distant_points = np.concatenate((lower, higher), axis=0)

        return distant_points

    # endregion

    # region VISUALISATION METHODS

    def draw(self):
        """Plot time series graph and save created graph to file."""
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # polting time series with legends and labels based on object 'name'
            if self.name == "amazon_stock_prices":
                plot_dataset.plot(rot=15, legend=False, xlabel="date", ylabel="stock price (USD)")
            elif self.name == "monthly_beer_production_in_austria":
                plot_dataset.plot(rot=15, legend=False, xlabel="date", ylabel="beer production (million HL)")

            # seting layout of figure
            plt.tight_layout()

        except Exception:
            print(f"TimeSeries.draw() ERROR \n{traceback.format_exc()}")
        else:
            # saving figure to file
            plt.savefig("timeseries.png", format="png", dpi=200)

    def draw_histogram(self):
        """Plot time series histogram and save created graph to file."""
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # ploting dataset histogram
            plot_dataset.hist()

        except Exception:
            print(f"TimeSeries.draw_histogram() ERROR \n{traceback.format_exc()}")
        else:
            # saving figure to file 
            plt.savefig("histogram.png")

    def draw_autocorelation(self, lags: int):
        """Plot autocorelation function of time series for given as 'lags' argument lag value."""
        try:

            # seting 'date' as index of dataset
            plot_dataset = self.data.set_index("date")

            # ploting autocorelation function
            plot_acf(plot_dataset, lags=lags)

        except Exception:
            print(f"TimeSeries.draw_autocorelation() ERROR \n{traceback.format_exc()}")
        else:
            # saving figure to file
            plt.savefig(f"autocorelation_{lags}.png")

    # endregion

    # region PRIVATE METHODS
    
    def _data_type_validation(self, dataset: pd.DataFrame) -> bool:
        """Checks if dataset has correct datatypes in columns and if all values are positive."""
        # checking types of data in columns
        if (dataset["date"].dtype == np.object) and (dataset["value"].dtype == np.float64):
            # checking if all values in 'value' column are higher than zero
            if dataset["value"].gt(0).all():
                return True
        else:
            return False
    
    def _data_complement(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Checks complementation of dataset and return corrected.
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
        """Unify 'value' column values of given dataset, by rounding all of them to one decimal place."""
        dataset = dataset.round(1)
        return dataset

    # endregion
