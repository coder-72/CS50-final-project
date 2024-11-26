from flask import render_template, Flask, request, url_for, session, flash, redirect
from flask_cors import CORS
from flask_session import Session
import utils
from werkzeug.exceptions import HTTPException, BadRequest
from api import api
from admin import admin
from auth import auth

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(auth)

@app.route("/")
def index():
    previews = utils.get_previews()
    return render_template("views/index.html", page_title="home", post_previews=previews, heading_image=url_for("static", filename="assets/img/compass-map.jpg"), title="Welcome to, travel.", subtitle="Welcome to my travel blog, have a look around", logged_in=utils.logged_in())

@app.route("/post/<int:post_id>")
def posts(post_id:int):
    post_content = utils.get_post(int(post_id))
    return render_template("views/post.html", page_title="post", title=post_content["title"], subtitle=post_content["subtitle"], heading_image=post_content["image"], date=utils.format_date(post_content["date"]), post_content=utils.markdown_to_html(post_content["content"]), logged_in=utils.logged_in())

@app.route("/search")
def search():
    if request.args.get("q"):
        query = request.args.get("q")
    else:
        query = ""

    return render_template("views/search.html", query=query, page_title="search", heading_image=url_for("static", filename="assets/img/travel-background.jpg"), logged_in=utils.logged_in())

@app.route("/about")
def about():
    return render_template("views/about.html", page_title="about",  heading_image=url_for("static", filename="assets/img/travel-essentials.jpg"), logged_in=utils.logged_in())

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("views/contact.html", page_title="contact", heading_image=url_for("static", filename="assets/img/contact-us.jpg"), logged_in=utils.logged_in())
    else:
        email = utils.valid_email(request.form["email"])
        if request.form["name"] and request.form["message"] and email:
            utils.send_email(request.form["name"], email, request.form["phone"], request.form["message"])
            flash("Thank you for contacting us!")
            return redirect("/")
        else:
            flash("Not all required form fields were filled")
            return render_template("views/contact.html", page_title="contact", heading_image=url_for("static", filename="assets/img/contact-us.jpg"), logged_in=utils.logged_in())



#@app.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time()), logged_in=utils.logged_in()), error_code



app.run(host='0.0.0.0', threaded=True)

