import os

DIR_PATH = os.path.dirname(__file__)

DEBUG = True

SERVER_NAME = '127.0.0.1:8000'

SECRET_KEY = 'lol'

DATABASE_URI = os.environ.get('DATABASE_URI',
    'sqlite:////{0}/requirements.db'.format(DIR_PATH))


# for GitHub auth
GH_CLIENT_ID = os.environ.get('GH_CLIENT_ID')
GH_CLIENT_SECRET = os.environ.get('GH_CLIENT_SECRET')