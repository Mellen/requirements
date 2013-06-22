import os

from flask import Flask
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
sentry.init_app(app)
# TODO: fix it to work on 'true' wsgi server
# app.config.from_object('requirements.settings')

import requirements.views
