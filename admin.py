from flask import Blueprint, request, render_template, flash, redirect
from werkzeug.exceptions import HTTPException
import utils

admin = Blueprint("admin", __name__, static_folder="static")


@admin.route("/")
@utils.login_required
def dashboard():
    html = utils.admin_articles()
    return render_template("admin/dashboard.html", html=html, page_title="dashboard", title="Dashboard", subtitle="Welcome back!", logged_in=utils.logged_in())

@admin.route("/add_post", methods=["GET", "POST"])
@utils.login_required
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
                flash("missing valid file or text", "error")
                return render_template("admin/add_post.html", page_title="Add post", title="Add post",subtitle="Add a new post", logged_in=utils.logged_in())
            utils.add_post(title, subtitle, image, markdown)
            flash("post successfully added!", "message")
            return redirect("/admin/")
        else:
            flash("title or image missing", "error")
            return render_template("admin/add_post.html", page_title="Add post", title="Add post",subtitle="Add a new post", logged_in=utils.logged_in())
            
    else:
        return render_template("admin/add_post.html", page_title="Add post", title="Add post",subtitle="Add a new post", logged_in=utils.logged_in())

@admin.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@utils.login_required
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
                flash("file or markdown missing", "error")
                return render_template("admin/edit_post.html", page_title="Edit post", title="Edit post",
                                   subtitle=post["title"], post=post, logged_in=utils.logged_in())
            utils.update_post(post_id, title, subtitle, image, markdown)
            post = utils.get_post(int(post_id))
            flash(f"post called {post[title]} successfully saved changes!", "message")
            return redirect("/admin/")
        else:
                flash("title ot image missing", "error")
                return render_template("admin/edit_post.html", page_title="Edit post", title="Edit post",
                                   subtitle=post["title"], post=post, logged_in=utils.logged_in())
    else:
        post = utils.get_post(post_id)
        return render_template("admin/edit_post.html", page_title="Edit post", title="Edit post",subtitle=post["title"], post=post, logged_in=utils.logged_in())


@admin.route("/preview", methods=["POST"])
@utils.login_required
def preview():
    markdown = request.form.get("markdown")
    title = request.form.get("title")
    subtitle = request.form.get("subtitle")
    image = request.form.get("image")
    return render_template("views/post.html", page_title="post preview", title=title, subtitle=subtitle, heading_image=image, date=utils.format_date(utils.get_time()), post_content=utils.markdown_to_html(markdown), logged_in=utils.logged_in())



@admin.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
        error_name = error.name
    else:
        error_code = 500
        error_name = "Server Error"

    print(error)
    return render_template('views/error.html',page_title=error_code, error=error, code=error_code, name=error_name, time=utils.format_date(utils.get_time()), logged_in=utils.logged_in()), error_code

