from flask import Blueprint, render_template
from .utils import shop_open
from .forms import ContactForm

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

@bp_main.route("/contact", methods=["GET", "POST"])   
def contact():
    form = ContactForm()
    if(form.validate_on_submit()):
        return "Form validated"
    return render_template("contact.html", form=form)

@bp_main.route("/about")   
def about():
    return render_template("about.html")