from flask import Blueprint, request, jsonify, session
from werkzeug.exceptions import HTTPException, BadRequest
import utils

#create blueprint
api = Blueprint("api", __name__, static_folder="static")

@api.route("/search")
def search():
    #get results for search query
    query = request.args.get("q")
    if query:
        posts = utils.search(query)
    else:
        posts = utils.search_all()
    posts_serializable = [dict(post) for post in posts]
    return jsonify({"results": posts_serializable})

@api.route("/mode", methods=["POST"])
def mode():
    #change theme (dark, auto, white)
    mode = request.json.get("mode")
    session["mode"] = mode
    print(mode)
    return jsonify(success=True)

@api.route("/delete", methods=["DELETE"])
@utils.login_required
def delete():
    #use delete func to delete user
    id = int(request.json.get("id"))
    utils.delete_post(id)
    print(id)
    return jsonify(success=True)

@api.errorhandler(Exception)
def error_handler(error):
    #handle error
    if isinstance(error, HTTPException):
        error_code = error.code
    else:
        error_code = 500
    print(error)
    return {}, error_code