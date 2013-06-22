
from flask.ext.sqlalchemy import SQLAlchemy

from requirements import app

db = SQLAlchemy(app)
db.init_app(app)

member_org_map = db.Table('member_org_map',
                          db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('org_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    github_access_token = db.Column(db.Integer)
    is_member = db.Column(db.Boolean)
    repos = []
    orgs = db.relationship('User',
                           secondary=member_org_map,
                           backref=db.backref('members', lazy='dynamic'))

<<<<<<< HEAD
    def __init__(self, username, github_access_token, is_member):
        self.username = username
=======
    def __init__(self, github_access_token):
>>>>>>> 17d3d91756caad7758099c1c8b6d2a0d68d585ec
        self.github_access_token = github_access_token
        self.is_member = is_member
        

    def __repr__(self):
        return '<User %s>' % self.username

    def update_repo_list(self):
        pass

class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_url = db.Column(db.String)

    def __init__(self):
        pass

class PyPiLibrary(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        pass

class Sync(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        pass

    
