from flask import g, render_template, request, redirect, session, url_for
from flask.ext.github import GithubAuth

from requirements import app
from requirements.models import db, User


github = GithubAuth(
    client_id=app.config.get('GH_CLIENT_ID'),
    client_secret=app.config.get('GH_CLIENT_SECRET'),
    session_key='user_id',
)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db.session.remove()
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/db_setup')
def db_setup():
    db.create_all()
    return 'ok'


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/oauth/callback')
@github.authorized_handler
def authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)

    token = resp['access_token']
    user = User.query.filter_by(github_access_token=token).first()
    if user is None:
        user = User(token)
        db.session.add(user)
    user.github_access_token = token
    db.session.commit()

    session['user_id'] = user.id

    return 'Success'


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize(callback_url=url_for('authorized'))
    else:
        return 'Already logged in'


@app.route('/orgs/<name>')
def orgs(name):
    if github.has_org_access(name):
        return 'Heck yeah he does!'
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
