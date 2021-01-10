import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_CONN_STR = os.getenv("MONGODB_CONN_STR")


class ProductionConfig(Config):
    # MONGODB_CONN_STR = os.getenv('MONGODB_CONN_STR')
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True