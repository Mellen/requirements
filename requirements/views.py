import sys

from flask import (
    render_template, request, redirect, session, url_for,
    jsonify, flash)

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


@app.route('/sync')
def sync():
    return 'sync here'


@app.route('/login')
def login():
    if session.get('github_token', None) is None:
        return github.authorize(callback=url_for('authorized', _external=True))
    else:
        flash("You're already logged in.", 'info')
        return redirect(url_for('sync'))


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    flash("You've successfully logged out.", 'info')
    return redirect(url_for('index'))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@app.route('/login/authorized')
@github.authorized_handler
def authorized(resp):
    if resp is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']), 'error')
    if 'access_token' in resp:
        token = (resp['access_token'], '')
        p(token)

        user = User.query.filter_by(access_token=token).first()
        if user is None:
            user = User(token)
            db.session.add(user)
        user.access_token = token
        db.session.commit()

        session['user_id'] = user.id
        session['github_token'] = token
        return redirect(url_for('sync'))
    return flash(str(resp), 'error')
