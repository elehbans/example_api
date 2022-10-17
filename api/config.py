import os

class Config(object):
    REDIS_SERVICE_NAME = os.environ['REDIS_SERVICE_NAME']
    REDIS_PORT = os.environ['REDIS_PORT']