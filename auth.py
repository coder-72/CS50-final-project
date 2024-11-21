from flask import Blueprint, request, render_template, abort
from werkzeug.exceptions import HTTPException
import utils

auth = Blueprint("auth", __name__, static_folder="static")

@auth.route("/login")
def login():
    return render_template("auth/login.html")



@auth.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time())), error_code

