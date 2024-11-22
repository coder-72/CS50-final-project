import bcrypt
from flask import Blueprint, request, render_template, abort, redirect, session, flash
from werkzeug.exceptions import HTTPException
import bcrypt
import utils

auth = Blueprint("auth", __name__, static_folder="static")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        user = utils.get_user(username)

        if user and bcrypt.checkpw(username.encode('utf-8'), user["password"].encode('utf-8')):
            session["user_id"] = user["id"]
        else:
            flash("Invalid username or password", "Error")
            return render_template("auth/login.html")
        return redirect("/")
    else:
        return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "message")
    return redirect("/")



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

