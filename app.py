from flask import render_template, Flask, request
import utils
import markdown2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("views/index.html", page_title ="title", )

@app.route("/post/<int:post_id>")
def posts(post_id:int):
    dict = utils.get_post(int(post_id))
    return render_template("")


app.run(debug=True)