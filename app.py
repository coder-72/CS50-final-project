from flask import render_template, Flask, request, url_for
from flask_cors import CORS
import utils
from werkzeug.exceptions import HTTPException, BadRequest
from api import api

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix="/api")

@app.route("/")
def index():
    previews = utils.get_previews()
    return render_template("views/index.html", page_title="Blog: home", post_previews=previews, heading_image=url_for("static", filename="assets/img/compass-map.jpg"))

@app.route("/post/<int:post_id>")
def posts(post_id:int):
    post_content = utils.get_post(int(post_id))
    return render_template("views/post.html", page_title="Blog: post", title=post_content["title"], subheading=post_content["subtitle"], heading_image=post_content["image"], date=utils.format_date(post_content["date"]), post_content=utils.markdown_to_html(post_content["content"]))

@app.route("/search")
def search():
    if request.args.get("q"):
        query = request.args.get("q")
    else:
        query = ""

    return render_template("views/search.html", query=query, page_title="Blog: Search", heading_image=url_for("static", filename="assets/img/travel-background.jpg"))

@app.route("/about")
def about():
    return render_template("views/about.html", page_title="Blog: about",  heading_image=url_for("static", filename="assets/img/travel-essentials.jpg"))

@app.route("/contact")
def contact():
    return render_template("views/contact.html", page_title="Blog: contact", heading_image=url_for("static", filename="assets/img/contact-us.jpg"))


@app.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time())), error_code



app.run(debug=True)
