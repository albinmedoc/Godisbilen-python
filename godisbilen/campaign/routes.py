import os
import secrets
from datetime import datetime
from flask import Blueprint, render_template, current_app, url_for, redirect, request
from flask_login import current_user
from godisbilen.app import db
from godisbilen.order_number import OrderNumber
from godisbilen.campaign import Campaign, CampaignOrder
from godisbilen.campaign.forms import JoinCampaignForm, CreateEditCampaignForm
from godisbilen.user import roles_accepted

bp_campaign = Blueprint("campaign", __name__)

@bp_campaign.route("/campaign/<int:campaign_id>", methods=["GET", "POST"])
def campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    # Don´t show campaign if it doesn´t exist or isn´t active for standard users
    if(not campaign or ((campaign.start > datetime.now() or campaign.end < datetime.now()) and (not current_user.is_authenticated or not current_user.has_roles("Admin")))):
        return redirect(url_for("main.home"))
    form = JoinCampaignForm()
    form.campaign_id.data = campaign_id
    if(form.validate_on_submit()):
        # Join campaign
        order = CampaignOrder.create(campaign=campaign, phone_number=form.phone_number.data, lat=form.lat.data, lng=form.lng.data)
        campaign.orders.append(order)
        db.session.commit()
        return redirect(url_for("campaign.confirmation", order_number=order.order_number.number))
    return render_template("campaign/campaign.html", campaign=campaign, form=form)

@bp_campaign.route("/campaign/confirmation/<order_number>")
def confirmation(order_number):
    order_number = OrderNumber.query.filter_by(number=order_number).first()
    if(not order_number):
        return "Ordern hittades inte"
    order = CampaignOrder.query.filter_by(order_number=order_number).first()
    if(not order):
        return "Kunde inte koppla ordernummret till en order"
    return render_template("campaign/confirmation.html", order=order)

@bp_campaign.route("/admin/create_campaign", methods=["GET", "POST"], endpoint="create")
@bp_campaign.route("/admin/edit_campaign/<int:campaign_id>", methods=["GET", "POST"], endpoint="edit")
@roles_accepted("Admin")
def create_edit(campaign_id=None):
    form = CreateEditCampaignForm()
    # Edit Campaign
    if(request.endpoint == "campaign.edit"):
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        if(not campaign):
            return "Erbjudandet hittades inte"
        form = CreateEditCampaignForm(title=campaign.title, info=campaign.info, terms=campaign.terms, start_date=campaign.start.date(), start_time=campaign.start.time(), end_date=campaign.end.date(), end_time=campaign.end.time(), delivery=campaign.delivery, per_user=campaign.per_user, per_address=campaign.per_address, amount=campaign.amount)
        form.image.validators = []
        form.submit.label.text = "Uppdatera"
    if(request.method == "POST"):
        if(form.validate_on_submit()):
            if(form.image.data):
                # Save image
                location = os.path.join(current_app.root_path, "static/img/campaign")
                filename = secrets.token_hex(8) + ".png"
                while os.path.isfile(os.path.join(location, filename)):
                    filename = secrets.token_hex(8) + ".png"

                # Checking if upload directory exists
                if(not os.path.exists(location)):
                    # Creating the directory if needed
                    os.makedirs(location)
                
                image = form.image.data
                image.save(os.path.join(location, filename))
            
            start = datetime.combine(form.start_date.data, form.start_time.data)
            end = datetime.combine(form.end_date.data, form.end_time.data)

            if(request.endpoint == "campaign.edit"):
                if(form.image.data):
                    campaign.image = filename
                campaign.title = form.title.data
                campaign.info = form.info.data
                campaign.terms = form.terms.data
                campaign.start = start
                campaign.end = end
                campaign.delivery = form.delivery.data
                campaign.per_user = form.per_user.data
                campaign.per_address = form.per_address.data
                campaign.amount = form.amount.data
            else:
                campaign = Campaign(title=form.title.data, image=filename, info=form.info.data, terms=form.terms.data, start=start, end=end, delivery=form.delivery.data, per_user=form.per_user.data, per_address=form.per_address.data, amount=form.amount.data)
                db.session.add(campaign)
            db.session.commit()
            return redirect(url_for("admin_route.home"))
    return render_template("campaign/create_edit_campaign.html", form=form)


@bp_campaign.route("/admin/campaign/home")
@roles_accepted("Admin")
def home():
    active_campaigns = Campaign.query.filter(Campaign.start < datetime.now(), Campaign.end > datetime.now()).all()
    upcomming_campaigns = Campaign.query.filter(Campaign.start > datetime.now()).all()
    passed_campaigns = Campaign.query.filter(Campaign.end < datetime.now()).all()
    return render_template("campaign/home.html", active_campaigns=active_campaigns, upcomming_campaigns=upcomming_campaigns, passed_campaigns=passed_campaigns)
