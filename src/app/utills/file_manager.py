import csv
import os

import pandas as pd


class FileManager:
    """Class that contains all file managements methods."""
    
    @staticmethod
    def read_file(file_name: str) -> pd.DataFrame:
        """Reads file, wchich name is given as 'file_name' argument,
        and returns this file content as pandas DataFrame."""
        path = os.path.join(file_name)
        return pd.read_csv(filepath_or_buffer=path)

    @staticmethod
    def save_file(file_name: str, data: pd.DataFrame):
        """Save given pandas DataFrame to file, wchich name is defined by 'file_name' argument."""
        path = os.path.join(file_name)
        data.to_csv(path_or_buf=path, index=False)
