## requirements

A little [Flask](<http://flask.pocoo.org/>) app to pull out dependency versions
for your Python projects located on [GitHub](<http://github.com/>).


### Quickstart

    git clone git@github.com:refreshoxford/requirements.git
    mkvirtualenv requirements
    pip install -r dev_requirements.txt
    gunicorn requirements:app
