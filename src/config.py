"""
Main configuration file.

This module contains all path to directories and files in module.
Credentials stored in this file shouldn't be commited to repository.
"""


import os


# ROOT APPLICATION DIRECTORY PATH
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# TEMPLATES DIRECTORY PATH
TEMPLATES_DIR = os.path.join(BASE_DIR, "app/templates")

# DATA DIRECTORY PATH
DATA_DIR = os.path.join(BASE_DIR, "data")

# RESULTS DIRECTORY PATH
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# LOGGING CONFIGURAION
LOGGING = {
    "CONFIG_FILE": f"{BASE_DIR}/.logs/logging.conf"
}