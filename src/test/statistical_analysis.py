"""
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf

from file_manager import FileManager


# 1. DATA PREPROCESSING

def data_type_validation(dataset: pd.DataFrame) -> bool:
    """Checks if timeseries dataset has correct datatypes in columns and if all values are positive."""
    # checking types of data in columns
    if (dataset["date"].dtype == np.object) and (dataset["value"].dtype == np.float64):
        # checking if all values in 'value' column are higher than zero
        if data["value"].gt(0).all():
            return True
    else:
        return False

def data_complement(dataset: pd.DataFrame) -> pd.DataFrame:
    """Checks complementation of dataset and return corrected.
    If 'data' column value is missing, removes row.
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


# 2. DESCRIPTIVE STATISTICS

def get_data_min_max(dataset: pd.DataFrame) -> (float, float):
    """Returns minimum and maximum values of timeseries dataset 'value' column."""
    return dataset["value"].min(), dataset["value"].max()

def get_data_average_and_standard_deviation(dataset: pd.DataFrame) -> (float, float):
    """Returns average and standard deviation values of timeseries dataset 'value' column."""
    return dataset["value"].mean(), dataset["value"].std()

def get_data_median(dataset: pd.DataFrame) -> float:
    """Returns median value of timeseries dataset 'value' column."""
    return dataset["value"].median()

def get_data_quantile(dataset: pd.DataFrame, q: int) -> float:
    """Returns given by 'q' argument quantile of timeseries dataset 'value' column."""
    return dataset["value"].quantile(q=q)

def get_data_interquartile(dataset: pd.DataFrame) -> float:
    """Returns interquartile value of timeseries dataset 'value' column.
    Inter quantile is difference between third and first quartile.
    """
    return stats.iqr(dataset["value"], interpolation="midpoint")


# 3. IDENTIFICATION OF DISTANT POINTS

def get_distant_points(dataset: pd.DataFrame) -> np.array:
    """Returns numpy array of distant points.
    Distant poinst are values lower than Q1 -1 or higher Q3 +1. 
    """

    q1 = get_data_quantile(dataset=dataset, q=0.25) - 1     # first quantile Q1 - 1
    q3 = get_data_quantile(dataset=dataset, q=0.75) + 1     # third quantile Q3 + 1

    # values lower than Q1 - 1
    lower = dataset.loc[dataset["value"] < q1]
    lower = lower["value"].values

    # values higher than Q3 + 1
    higher = dataset.loc[dataset["value"] > q3]
    higher = higher["value"].values

    # concating two numpy arrays
    distant_points = np.concatenate((lower, higher), axis=0)

    return distant_points


# 4. AUTO CORRELATION COEFFICIENT

def draw_autocorelation(dataset: pd.DataFrame, lags: int):
    """Draw autocorelation function of given dataset with given 'lags' value."""
    plot_dataset = dataset.set_index("date")    # seting 'date' as index of dataset
    plot_acf(plot_dataset, lags=lags)   # ploting autocorelation function
    plt.savefig(f"autocorelation_{lags}.png")   # saving figure to file


# 5. LINEAR REGRESION

def draw_linear_regression(dataset: pd.DataFrame):
    """"""
    pass


# 6. DATA VISUALISATION

def draw_timerseries(dataset: pd.DataFrame, filename: str):
    """Draw timeseries given by 'dataset' argument."""
    plot_dataset = dataset.set_index("date")    # seting 'date' as index of dataset

    # polting timeseries with legends and labels based on 'file_name' argument value
    if filename == "amazon_stock_prices.csv":
        plot_dataset.plot(rot=15, legend=False, xlabel="date", ylabel="stock price (USD)")
    elif filename == "monthly_beer_production_in_austria.csv":
        plot_dataset.plot(rot=15, legend=False, xlabel="date", ylabel="beer production (million HL)")

    plt.tight_layout()  # seting layout of figure
    plt.savefig("timeseries.png", format="png", dpi=200)    # saving figure to file

def draw_timeseries_histogram(dataset: pd.DataFrame):
    """Draw given dataset 'value' column histogram."""
    plot_dataset = dataset.set_index("date")    # seting 'date' as index of dataset
    plot_dataset.hist()     # ploting dataset histogram
    plt.savefig("histogram.png")    # saving figure to file 


# MAIN SECTION

file_name = "amazon_stock_prices.csv"
data = FileManager.read_file(file_name)

print()
print("Making dataset complementation")
data = data_complement(dataset=data)

print()
print(f"Dataset type validation results = {data_type_validation(dataset=data)}")

minimum, maximum = get_data_min_max(dataset=data)
print()
print(f"Minimum value = {minimum}")
print(f"Maximum value = {maximum}")

average, std = get_data_average_and_standard_deviation(dataset=data)
print()
print(f"Average value = {average}")
print(f"Standard deviation = {std}")

median = get_data_median(dataset=data)
print()
print(f"Meidan value = {average}")

print()
print(f"0.1 quantile value = {get_data_quantile(dataset=data, q=0.1)}")
print(f"0.9 quantile value = {get_data_quantile(dataset=data, q=0.9)}")

interquartile = get_data_interquartile(dataset=data)
print()
print(f"Interquartile = {interquartile}")

distant_points = get_distant_points(dataset=data)
print()
print(f"Distant points = {distant_points}")

draw_timerseries(dataset=data, filename=file_name)
draw_autocorelation(dataset=data, lags=100)
draw_timeseries_histogram(dataset=data)
