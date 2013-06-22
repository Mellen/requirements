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
    repos = db.relationship('Repo',
                            backref=db.backref('user', lazy='joined'),
                            lazy='dynamic')
    orgs = db.relationship('User',
                           secondary=member_org_map,
                           backref=db.backref('members', lazy='dynamic'))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

    def __repr__(self):
        return '<User %s>' % self.username

class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String, unique=True)
    version = db.Column(db.String)
    last_fetch_date_time = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)

class Sync(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    last_sync_date_time = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)
    last_sync_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
