import os
from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    basedir    = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'arif'
    DB_HOST = "127.0.0.1"
    DB_NAME = "image_comparison_db"
    DB_USERNAME = "root"
    DB_PASSWORD = "root1234"
    UPLOADS = "D:/MYSELF/pancardtampering/app/static/uploads"
    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None
    ENV = "production"

class ProductionConfig(Config):
    pass 

class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = '127.0.0.1'
    DB_NAME = "image_comparison_db"
    DB_USERNAME = "root"
    DB_PASSWORD = "root1234"
    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False
    ENV = "development"

class TestingConfig(Config):
    DEBUG = True
    DB_HOST = '127.0.0.1'
    DB_NAME = "image_comparison_db"
    DB_USERNAME = "root"
    DB_PASSWORD = "root1234"
    UPLOADS = "/home/username/app/app/static/uploads"   
    SESSION_COOKIE_SECURE = False # only https connections

class DebugConfig(Config):
    DEBUG = True
    env="development"    
