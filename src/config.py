"""
Main configuration file.

This module contains all path to directories and files in module.
Credentials stored in this file shouldn't be commited to repository.
"""


import os


# ROOT APPLICATION DIRECTORY PATH
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# LOGGING CONFIGURAION
LOGGING = {
    "CONFIG_FILE": f"{BASE_DIR}/.logs/logging.conf"
}