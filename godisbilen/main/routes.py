from flask import Blueprint, render_template
from .utils import shop_open

bp_main = Blueprint("main", __name__)

@bp_main.route("/")
def home():
    return render_template("home.html", shop_open=shop_open())

@bp_main.route("/working_areas")   
def working_areas():
    return render_template("working_areas.html")

@bp_main.route("/tos")   
def tos():
    return render_template("tos.html")

@bp_main.route("/contact")   
def contact():
    return render_template("contact.html")

@bp_main.route("/about")   
def about():
    return render_template("about.html")