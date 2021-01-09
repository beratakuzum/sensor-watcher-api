import logging

import config
import os

from flask import Flask
from werkzeug.utils import import_string

from src.utils.errors import init_error_handler
from src.db.mongodb import MongoDB
from src.apis.sensors import sensors_bp

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)

    # get config
    env_dispatcher = {
        "production": "ProductionConfig",
        "testing": "TestingConfig",
        "development": "DevelopmentConfig"
    }
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    config_class = env_dispatcher[FLASK_ENV]
    logging.info("running in " + FLASK_ENV + " mode")

    cfg = import_string(f'config.{config_class}')()
    app.config.from_object(cfg)

    # register_db
    app.mongo_db = MongoDB(app.config['MONGODB_CONN_STR'])

    # register bluprints
    app.register_blueprint(sensors_bp, url_prefix='/sensors')

    # register custom error handler
    init_error_handler(app)
    logging.info("server_name: " + app.config['SERVER_NAME'])
    return app
