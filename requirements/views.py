import sys

from flask import (
    render_template, request, redirect, session, url_for,
    jsonify)

from requirements import app
from requirements.github import github
from requirements.models import db, User


def p(s):
    print s
    sys.stdout.flush()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/db_reset')
def db_reset():
    db.drop_all()
    db.create_all()

    return 'ok'


@app.route('/create_user/<token>')
def create_user(token):
    user = User(token)
    db.session.add(user)
    db.session.commit()

    return 'ok'


@app.route('/dataz')
def dataz():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@app.route('/login/authorized')
@github.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    return jsonify(me.data)


@app.route('/login')
def login():
    if session.get('github_token', None) is None:
        return github.authorize(callback=url_for('authorized', _external=True))
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/orgs/<name>')
def orgs(name):
    if github.has_org_access(name):
        return 'Heck yeah he does!'
    else:
        return redirect(url_for('index'))
