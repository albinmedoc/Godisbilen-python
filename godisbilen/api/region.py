
from flask import jsonify
from flask_cors import cross_origin
from .auth import auth
from godisbilen.region import Region

@cross_origin()
@auth.login_required
def get_regions():
    return Region.get_bounds(active=True, lat_lng=True)

@cross_origin()
@auth.login_required
def get_region(region_name):
    return Region.get_bounds(active=True, regions=[region_name], lat_lng=True)
