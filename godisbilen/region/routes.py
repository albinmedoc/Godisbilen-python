from flask import Blueprint, request, jsonify
from .region import Region

bp_region = Blueprint("regions", __name__)

@bp_region.route("/get_region_boundaries", methods=["POST"])
def get_region_bounds():
    active = request.values.get("active", default=True)
    print(active)
    return jsonify(Region.get_bounds(lat_lng=True, active=active))