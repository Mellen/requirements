from flask_oauthlib.client import OAuth

from requirements import app

oauth = OAuth(app)


github = oauth.remote_app(
    'github',
    consumer_key=app.config.get('GH_CLIENT_ID'),
    consumer_secret=app.config.get('GH_CLIENT_CLIENT'),
    request_token_params={'scope': 'repo'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)
