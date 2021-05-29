"""
Files manager script

This script contains FileManager class responsible for managing files in this application.
"""


import config
import os
import traceback

import pandas as pd
from flask import Request
from werkzeug.utils import secure_filename

import app


class FileManager:
    """Class that contains all file managements methods."""
    
    @staticmethod
    def read_file(file_name: str) -> pd.DataFrame:
        """Reads file, which name is given by 'file_name' argument,
        and returns content of this file as pandas DataFrame object."""
        path = os.path.join(file_name)
        return pd.read_csv(filepath_or_buffer=path)

    @staticmethod
    def save_file(file_name: str, data: pd.DataFrame):
        """Save given pandas DataFrame object to csv file,
        wchich name is defined by 'file_name' argument."""
        path = os.path.join(file_name)
        data.to_csv(path_or_buf=path, index=False)

    @staticmethod
    def upload_file(request: Request) -> str:
        """Uploads file received by request to application data directory, 
        saves it and returns absolute path to this file."""
        try:

            # retrieves file from request
            _file = request.files["file"]

            # absoulte path to file
            file_path = os.path.join(config.DATA_DIR, secure_filename(_file.filename))

            # saves received file
            _file.save(file_path)

        except Exception:
            app.logging.error(f"FileManager.upload_file() -> {traceback.format_exc()}")
            return ""
        else:
            app.logging.info("file uploaded successfully!")
            return file_path