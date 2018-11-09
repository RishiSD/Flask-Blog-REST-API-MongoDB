import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Z\xf0\xfb\xf0r\x8c\r\xa4\xc6Qf\xc2\x15\xcb\x12')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'flask-mongo-api')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://rishid:Mongo_11!@ds115613.mlab.com:15613/flask-mongo-api')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
