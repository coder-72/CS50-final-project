from flask import Flask, render_template, Blueprint
from werkzeug.exceptions import HTTPException
from blueprints.api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/_api")

@app.route('/')
def index():
    return render_template('views/index.html', loggedIn = False)

@app.route('/search')
def search():
    return render_template('views/search.html', loggedIn = False)

@app.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
    else:
        error_code = 500
    print(error)

    return render_template('views/error.html', error=error, code=error_code)


if __name__ == '__main__':
    app.run(debug=True)