import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Z\xf0\xfb\xf0r\x8c\r\xa4\xc6Qf\xc2\x15\xcb\x12')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'test')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/test')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
