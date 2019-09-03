import json
import os
from flask import current_app
from shapely.geometry import Point, Polygon
import googlemaps


def get_city_boundaries(cities=None):
    dir_city_bounds = os.path.join(
        current_app.root_path, "static/city_boundaries")
    if(not cities):
        # No cities choosen, add all to list
        cities = [os.path.splitext(f)[0] for f in os.listdir(dir_city_bounds) if os.path.isfile(
            os.path.join(dir_city_bounds, f)) and f.endswith(".json")]

    temp = {}
    for city in cities:
        if(not os.path.isfile(os.path.join(dir_city_bounds, city + ".json"))):
            temp[city] = []
            continue
        with current_app.open_resource(os.path.join(dir_city_bounds, city + ".json")) as file:
            temp[city] = json.load(file)
    return temp


def coords_in_working_area(lat, lng):
    point = Point(lat, lng)
    city_boundaries = get_city_boundaries()

    inside = False
    for city in city_boundaries:
        city_boundary = []
        for coord in city_boundaries[city]:
            city_boundary.append((coord["lat"], coord["lng"]))
        city_boundary = Polygon(city_boundary)
        if(city_boundary.contains(point)):
            inside = True
    return inside


def get_city_from_coords(lat, lng):
    point = Point(lat, lng)
    city_boundaries = get_city_boundaries()

    for city in city_boundaries:
        city_boundary = []
        for coord in city_boundaries[city]:
            city_boundary.append((coord["lat"], coord["lng"]))
        city_boundary = Polygon(city_boundary)
        if(city_boundary.contains(point)):
            return city
    return None


def get_time_between(origin, destination):
    gmaps = googlemaps.Client(key=current_app.config["GOOGLE_MAPS_API_KEY"])
    data = gmaps.distance_matrix(origin, destination, mode="driving")
    if(data["status"] == "OK"):
        return data["rows"][0]["elements"][0]["duration"]["value"]
    return 600
