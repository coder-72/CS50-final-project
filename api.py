from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException, BadRequest
import utils

api = Blueprint("api", __name__, static_folder="static")

@api.route("/search")
def search():
    query = str(request.args.get("q"))
    posts = None
    if not query:
        posts = utils.search_all()
    else:
        posts = utils.search(query)

    posts_serializable = [dict(post) for post in posts]
    #print(posts_serializable)
    return jsonify({"results": posts_serializable})

@api.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
    else:
        error_code = 500
    print(error)
    return {}, error_code