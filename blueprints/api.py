from flask import Blueprint, request
import requests

api = Blueprint("api", __name__)
api_key = "ec7da2f04ea144b9a84565e8e9cafdf4"

@api.route("/search/all", methods=["GET"])
def search_all():
    q = request.args.get("q")
    return requests.get("https://api.spoonacular.com/food/search", params={"query" : q, "number" : 100, "apiKey" : api_key}).json()


