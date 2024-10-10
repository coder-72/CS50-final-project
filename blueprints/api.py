from flask import Blueprint, request
import requests
from werkzeug.exceptions import HTTPException

api = Blueprint("api", __name__, static_folder="static")
api_key = "ec7da2f04ea144b9a84565e8e9cafdf4"

@api.route("/search/all", methods=["GET"])
def search_all():
    q = request.args.get("q")
    print("api accessed")
    return requests.get("https://api.spoonacular.com/food/search", params={"query" : q, "number" : 100, "apiKey" : api_key}).json()

@api.route("/search/recipes", methods=["GET"])
def search_recipes():
    q = request.args.get("q")
    print("api accessed")
    return requests.get("https://api.spoonacular.com/recipes/complexSearch", params={"query" : q, "number" : 100, "apiKey" : api_key}).json()


@api.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, HTTPException):
        error_code = error.code
    else:
        error_code = 500
    print(error)
    return {}, error_code