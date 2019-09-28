from flask import Blueprint, request, jsonify
from godisbilen.region import Region

bp_loc = Blueprint("loc", __name__)

@bp_loc.route("/get_city_boundaries", methods=["POST"])
def get_city_bounds():
    Region.get_bounds()
    cities = request.values.getlist("city", type=str)
    return jsonify(Region.get_bounds(lat_lng=True))