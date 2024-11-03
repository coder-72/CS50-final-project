from flask import Blueprint, request, jsonify, session
from werkzeug.exceptions import HTTPException, BadRequest
import utils

api = Blueprint("api", __name__, static_folder="static")

@api.route("/search")
def search():
    query = request.args.get("q")
    if query:
        posts = utils.search(query)
    else:
        posts = utils.search_all()
    posts_serializable = [dict(post) for post in posts]
    return jsonify({"results": posts_serializable})

@api.route("/mode", methods=["POST"])
def mode():
    mode = request.json.get("mode")
    session["mode"] = mode
    print(mode)
    return jsonify(success=True)

@api.route("/delete", methods=["DELETE"])
def delete():
    id = int(request.json.get("id"))
    print(id)
    return jsonify(success=True)

@api.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
    else:
        error_code = 500
    print(error)
    return {}, error_code