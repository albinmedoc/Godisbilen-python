from flask import Blueprint, request, jsonify
from godisbilen.location.utils import get_city_boundaries

bp_loc = Blueprint("loc", __name__)

@bp_loc.route("/get_city_boundaries", methods=["POST"])
def get_city_bounds():
    cities = request.values.getlist("city", type=str)
    return jsonify(get_city_boundaries(cities))