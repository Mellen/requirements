from flask import Flask

app = Flask(__name__)
# TODO: fix it to work on 'true' wsgi server
# app.config.from_object('requirements.settings')

import requirements.views
