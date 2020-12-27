import flask
import flask_restful
import logging
import logging.config
import os
import warnings
import yaml

import app
import config


# disabling startup warnings
warnings.filterwarnings('ignore')
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.ERROR)


# application logging configuration, based on logging.cfg file
logging.config.dictConfig(yaml.load(open(config.LOGGING["CONFIG_FILE"])))


# application and api main instances
APP = flask.Flask(__name__)
API = flask_restful.Api(APP)


# application file upload folder configuration
APP.config["UPLOAD_FOLDER"] = config.STATIC_DIR


# application secret key
APP.secret_key = os.urandom(24)


from app import routes
from app import errors
