from flask import Blueprint, request, render_template, abort
from werkzeug.exceptions import HTTPException
import utils

admin = Blueprint("admin", __name__, static_folder="static")

@admin.route("/")
def dashboard():
    html = utils.admin_articles()
    return render_template("admin/dashboard.html", html=html, page_title="dashboard", title="Dashboard", subtitle="Welcome back!")

@admin.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        file = request.files.get("file")
        text = request.form.get("markdown", "")
        title = request.form.get("title")
        subtitle = request.form.get("subtitle", "")
        image = request.form.get("image")
        if  title and image:
            if file and utils.allowed_file(file.filename):
                markdown = file.read().decode("utf-8")
            elif text:
                markdown = text
            else:
                abort(500, description="file or markdown required")
            utils.add_post(title, subtitle, image, markdown)
            return render_template("admin/add_post.html", page_title="Add post", title="Add post",
                                   subtitle="Add a new post", show_thanks=True)
        else:
            abort(500, description="title and image is required")
    else:
        return render_template("admin/add_post.html", page_title="Add post", title="Add post",subtitle="Add a new post", show_thanks=False)

@admin.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        text = request.form.get("markdown", "")
        title = request.form.get("title")
        subtitle = request.form.get("subtitle", "")
        image = request.form.get("image")
        if title and image:
            if text:
                markdown = text
            else:
                abort(500, description="file or markdown required")
            utils.update_post(post_id, title, subtitle, image, markdown)
            post = utils.get_post(int(post_id))
            return render_template("admin/edit_post.html", page_title="Edit post", title="Edit post",
                                   subtitle=post["title"], post=post)
        else:
            abort(500, description="title and image is required")
    else:
        post = utils.get_post(post_id)
        return render_template("admin/edit_post.html", page_title="Edit post", title="Edit post",subtitle=post["title"], post=post)


@admin.route("/preview", methods=["POST"])
def preview():
    markdown = request.form.get("markdown")
    title = request.form.get("title")
    subtitle = request.form.get("subtitle")
    image = request.form.get("image")
    return render_template("views/post.html", page_title="post preview", title=title, subtitle=subtitle, heading_image=image, date=utils.format_date(utils.get_time()), post_content=utils.markdown_to_html(markdown))



@admin.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time())), error_code

