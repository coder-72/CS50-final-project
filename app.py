from flask import render_template, Flask, request
import utils

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("views/index.html", page_title="blog-home page", )

@app.route("/post/<int:post_id>")
def posts(post_id:int):
    dict = utils.get_post(int(post_id))
    return render_template("views/post.html", page_title="blog-post", title=dict["title"], subheading=dict["subtitle"], date=utils.format_date(dict["date"]), image=dict["image"], post_content=utils.markdown_to_html(dict["content"]))


app.run(debug=True)