import os
from flask import Blueprint, render_template, current_app, url_for
from flask_mail import Message
from .utils import shop_open
from .forms import ContactForm
from godisbilen.app import mail

bp_main = Blueprint("main", __name__)

@bp_main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(current_app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@bp_main.route("/")
def home():
    return render_template("main/home.html", shop_open=shop_open())

@bp_main.route("/regions")   
def regions():
    return render_template("main/regions.html")

@bp_main.route("/tos")   
def tos():
    return render_template("main/tos.html")

@bp_main.route("/contact", methods=["GET", "POST"])   
def contact():
    form = ContactForm()
    if(form.validate_on_submit()):
        msg = Message(subject=form.subject.data, recipients=[current_app.config["MAIL_DEFAULT_SENDER"]])
        msg.body = "Meddelande från " + form.name.data + "(" + form.email.data + ")" + ". Innehåll: " + form.message.data
        if(form.order_number.data.strip() != ""):
            msg.body = msg.body + ". Ordernummer: " + form.order_number.data
        mail.send(msg)
        return render_template("main/contact.html", form=form, message_sent=True)
    return render_template("main/contact.html", form=form)

@bp_main.route("/about")   
def about():
    return render_template("main/about.html")