import bcrypt
from flask import Blueprint, request, render_template, abort, redirect, session, flash
from werkzeug.exceptions import HTTPException
import bcrypt
import utils

#create blueprint
auth = Blueprint("auth", __name__, static_folder="static")

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    login route excepts ,form with post method
    """
    #check method
    if request.method == "POST":
        #if post check user details if correct login
        username = request.form["username"]
        password = request.form["password"]
        user = utils.get_user(username)

        if user and bcrypt.checkpw(username.encode('utf-8'), user["password"].encode('utf-8')):
            session.pop("user_id", None)
            session["user_id"] = user["id"]
        else:
            #if invalid render login again and flash message
            flash("Invalid username or password", "Error")
            return render_template("auth/login.html", title = "Login",subtitle="Login to admin account.", page_title = "Login", logged_in=utils.logged_in())
        flash("login successful", "message")
        return redirect("/admin/")
    else:
        #if get method then just return html template
        return render_template("auth/login.html", title = "Login",subtitle="Login to admin account.", page_title = "Login", logged_in=utils.logged_in())
    
@auth.route("/logout")
def logout():
    #logout user before redirecting them to the home page and flashing message
    session.clear()
    flash("Successfully logged out!", "message")
    return redirect("/")



@auth.errorhandler(Exception)
def error_handler(error):
    #handles errors and displays them to user
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time()), logged_in=utils.logged_in()), error_code

