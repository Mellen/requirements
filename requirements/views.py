from flask import render_template

from requirements import app


@app.route('/')
def index():
    return render_template('index.html')
