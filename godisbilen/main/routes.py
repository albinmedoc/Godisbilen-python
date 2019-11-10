from datetime import datetime
from flask import Blueprint, render_template, current_app, url_for
from flask_mail import Message
from .utils import shop_open
from .forms import ContactForm
from godisbilen.app import mail, db
from godisbilen.user import User
from godisbilen.location import Location
from godisbilen.campaign import Campaign, CampaignUsers
from godisbilen.campaign.forms import JoinCampaignForm

bp_main = Blueprint("main", __name__)

@bp_main.route("/")
def home():
    campaigns = Campaign.query.filter(Campaign.start < datetime.now(), Campaign.end > datetime.now()).all()
    return render_template("main/home.html", shop_open=shop_open(), campaigns=campaigns)

@bp_main.route("/campaign/<int:campaign_id>", methods=["GET", "POST"])
def campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    if(not campaign):
        return "Erbjudandet hittades inte"
    form = JoinCampaignForm()
    form.campaign_id.data = campaign_id
    if(form.validate_on_submit()):
        # Join campaign
        user = User.query.filter_by(phone_number=form.phone_number.data).first()
        if(not user):
            user = User(phone_number=phone_number)
            db.session.add(user)
        location = Location.query.filter_by(lat=form.lat.data, lng=form.lng.data).first()
        if(not location):
            location = Location(lat=orm.lat.data, lng=form.lng.data)
            db.session.add(location)
        campaign.buyers.append(CampaignUsers(campaign_id=campaign_id, user=user, location=location))
        db.session.commit()
        return "Order lagd"
    return render_template("main/campaign.html", campaign=campaign, form=form)

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

@bp_main.route("/faq")   
def faq():
    return render_template("main/faq.html")