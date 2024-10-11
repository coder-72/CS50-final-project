from flask import render_template, Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("views/index.html", page_title ="title", )

@app.route("/post")
def posts():
    id = request.args.get("id")


app.run(debug=True)