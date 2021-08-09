import config
import logging
import logging.config
import warnings

import flask
import flask_restful
import yaml


# disabling startup warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", "statsmodels.tsa.ar_model.AR", FutureWarning)
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
APP.secret_key = "5b0a1a0d6f2a4fbc9f1d9a8bb8ed638f"

# disabling image caching
APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


from app import routes
from app import errors
