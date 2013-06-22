from flask.ext.sqlalchemy import SQLAlchemy
from requirements import app

db = SQLAlchemy(app)
db.init_app(app)

member_org_map = db.Table('member_org_map', 
                          db.Column('member_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                          db.Column('org_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    github_access_token = db.Column(db.Integer)
    is_member = db.Column(db.Boolean)
    repos = db.relationship('Repo',
                            backref=db.backref('user', lazy='joined'),
                            lazy='dynamic')
    orgs = db.relationship('User',
                           secondary=member_org_map,
                           primaryjoin=id==member_org_map.c.member_id,
                           secondaryjoin=id==member_org_map.c.org_id,
                           backref='members', lazy='dynamic')

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

    def __repr__(self):
        return '<User {0}, ({1})>'.format(self.username, 'member' if self.is_member else 'organisation')

class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requirements = db.Column(db.Text)
    def __repr__(self):
        return '<Repo {0}>'.format(self.repo_name)


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String, unique=True)
    version = db.Column(db.String)
    last_fetch_date_time = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)

    def __repr__(self):
        return '<Package {0} {1} {2}>'.format(self.package, self.version, self.last_fetch_date_time)

class Sync(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    last_sync_date_time = db.Column(db.DateTime, default=db.func.now, onupdate=db.func.now)
    last_sync_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    
