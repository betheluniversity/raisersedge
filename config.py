import os


class BaseConfig(object):
    CONSTR = os.environ['CONSTR']
    APPLICATION_ID = os.environ['APPLICATION_ID']
    APPLICATION_SECRET = os.environ['APPLICATION_SECRET']
    SUBSCRIPTION_KEY = os.environ['SUBSCRIPTION_KEY']
    AUTH_REDIRECT_URL = os.environ['AUTH_REDIRECT_URL']
    TOKEN_URL = os.environ['TOKEN_URL']
    API_URL = os.environ['API_URL']

    LOGIN_URL = os.environ['LOGIN_URL']
    LOGIN_URL %= (APPLICATION_ID, AUTH_REDIRECT_URL)

    LOGIN_TABLE = os.environ['LOGIN_TABLE']

    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True