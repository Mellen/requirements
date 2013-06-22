import json
import sys

from flask import (
    render_template, request, redirect, session, url_for,
    jsonify, flash)

from requirements import app
from requirements.github import github
from requirements.models import db, User, Repo


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/testdata')
def testdata():
    db.drop_all()
    db.create_all()
    me = User('blah1')
    me.username = 'Mellen'
    me.is_member = True
    
    notme = User('blah3')
    notme.username = 'Keith'
    notme.is_member = True

    ro = User('blah2')
    ro.username = 'Refresh Oxford'
    ro.is_member = False

    repo1 = Repo()
    repo1.repo_name = 'Mellen\'s first repo'

    db.session.add(me)
    db.session.add(notme)
    db.session.add(ro)
    db.session.add(repo1)
    db.session.commit()

    me.repos.append(repo1)

    ro.members.append(me)
    ro.members.append(notme)

    db.session.commit()
    
    result = '{0}, {1}, {2}'.format(str(me), str(ro), str(repo1)).replace('<', '&lt;')
    result += '<br>'
    result += "Mellen's repo is called '{0}'".format(str(me.repos[0])).replace('<', '&lt;')
    result += '<br>'
    result += "{0} is member of {1}".format(str(me), str(me.orgs[0])).replace('<', '&lt;')
    result += '<br>'
    for member in ro.members:
        result += "{0} has member {1} <br>".format(str(ro), str(member)).replace('<', '&lt;')
    return result

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


def _get_repos(data):
    _repos = {}
    data = json.loads(data.raw_data)
    for x in data:
        if x['language'] and x['language'].lower() == 'python':
            key = x['owner']['login']
            l = [{
                'name': x['name'],
                'url': x['html_url'],
            }]
            if key in _repos:
                _repos[key].append(l[0])
            else:
                _repos[key] = l
    return _repos


@app.route('/sync')
def sync():
    if 'github_token' in session:
        user_repos = github.get('user/repos')
        user_repos = _get_repos(user_repos)

        orgs = github.get('user/orgs')
        for x in json.loads(orgs.raw_data):
            org_repos = github.get('orgs/{0}/repos'.format(x['login']))
            org_repos = _get_repos(org_repos)
            user_repos = dict(user_repos, **org_repos)

        return jsonify(user_repos)
    return redirect(url_for('login'))


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


@app.route('/login/authorized')
@github.authorized_handler
def authorized(resp):
    if resp is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']), 'error')

    if 'access_token' in resp:
        token = (resp['access_token'], '')

        user = User.query.filter_by(access_token=token[0]).first()
        if user is None:
            user = User(token[0])
            db.session.add(user)
        user.access_token = token[0]
        db.session.commit()

        session['user_id'] = user.id
        session['github_token'] = token
        return redirect(url_for('sync'))
    return flash(str(resp), 'error')


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')
