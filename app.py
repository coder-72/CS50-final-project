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
    """
    home page of the website including featured posts.

    Parameters
    ----------
        non

    Returns
    -------
        webpage (templates/veiws/index.html)

    Raises
    ------
        Exception
            if files don't exist
            if database doesn't exist
    """

    #get preveiw html of most recent posts
    previews = utils.get_previews()
    #returns the webpage
    return render_template("views/index.html", page_title="home", post_previews=previews, heading_image=url_for("static", filename="assets/img/compass-map.jpg"), title="Welcome to, travel.", subtitle="Welcome to my travel blog, have a look around", logged_in=utils.logged_in())

@app.route("/post/<int:post_id>")
def posts(post_id:int):
    """
    Shows individual post.

    Params
    -------
    post_id : int
        the id of the post to display

    Returns
    -------
        webpage (templates/veiws/post.html)

    Raises
    ------
        Exception
            if post id isn't an integer or the id of a post int the db
            if html file doesn't exist
    """

    #get post content from posts table in blog.db
    post_content = utils.get_post(int(post_id))
    #returns the webpage
    return render_template("views/post.html", page_title="post", title=post_content["title"], subtitle=post_content["subtitle"], heading_image=post_content["image"], date=utils.format_date(post_content["date"]), post_content=utils.markdown_to_html(post_content["content"]), logged_in=utils.logged_in())

@app.route("/search")
def search():
    """
    search function for posts using sql FTS.

    Params
    ------
        Non

    Returns
    -------
        webpage (templates/veiws/search.html)
    
    Raises
    -------
        Exception
            if image or html file doesn't exist
    """

    #check if query param was given in url if not set it to blank
    if request.args.get("q"):
        query = request.args.get("q")
    else:
        query = ""

    #returns the webpage
    return render_template("views/search.html", query=query, page_title="search", heading_image=url_for("static", filename="assets/img/travel-background.jpg"), logged_in=utils.logged_in())

@app.route("/about")
def about():
    """
    About website and posts

    Params
    ------
        Non
    
    Returns
    -------
        webpage (templates/views/about.html)
    
    Raises
    ------
        Exception
            if image file or html file deleted
    """

    # returns about webpage with extra params for title, header image, etc.
    return render_template("views/about.html", page_title="about",  heading_image=url_for("static", filename="assets/img/travel-essentials.jpg"), logged_in=utils.logged_in())

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    contact form for blog
    sends email to all admin account emails

    Params
    ------
        Non
    
    Returns
    -------
        webpage (templates/views/contact.html)
    
    Raises
    ------
        Exception
            if image file or html file deleted
    """

    #checks method used to get page if get post processes form
    if request.method == "GET":
        return render_template("views/contact.html", page_title="contact", heading_image=url_for("static", filename="assets/img/contact-us.jpg"), logged_in=utils.logged_in())
    else:
        email = utils.valid_email(request.form["email"])

        # checks that form fields that are needed exist
        if request.form["name"] and request.form["message"] and email:
            utils.send_email(request.form["name"], email, request.form["phone"], request.form["message"])
            flash("Thank you for contacting us!")
            return redirect("/")
        else:
            #prompts user if not all fields filled
            # returns about webpage with extra params for title, header image, etc.
            flash("Not all required form fields were filled")
            return render_template("views/contact.html", page_title="contact", heading_image=url_for("static", filename="assets/img/contact-us.jpg"), logged_in=utils.logged_in())



#@app.errorhandler(Exception)
def error_handler(error):
    """
    handles any errors that occur and displays it to the user

    Params
    ------
        error
    
    Returns
    -------
        webpage (templates/views/error.html)
    
    Raises
    ------
        Non
    """

    # check if http error if not makes it an internal server error code (500)
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time()), logged_in=utils.logged_in()), error_code


#run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)

