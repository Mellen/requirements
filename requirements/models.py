
from flask.ext.sqlalchemy import SQLAlchemy

from requirements import app

db = SQLAlchemy(app)
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    github_access_token = db.Column(db.Integer)

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

    def __repr__(self):
        return '<User %s>' % self.username
