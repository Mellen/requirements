import os

from flask import Flask
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_object('requirements.settings')

sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
sentry.init_app(app)

from requirements.views import *
