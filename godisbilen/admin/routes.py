import os
import secrets
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from sqlalchemy import func
from godisbilen.app import db
from godisbilen.order import Order
from godisbilen.purchase import PurchaseForm, PurchaseProducts, Purchase
from godisbilen.product import Product
from godisbilen.region import Region
from godisbilen.user import User, roles_accepted
from godisbilen.admin import Admin
from godisbilen.admin.forms import AdminLoginForm, AdminRegisterForm, AdminRegionForm
from godisbilen.campaign import Campaign, CampaignProducts
from godisbilen.campaign.forms import CreateCampaignForm

bp_admin = Blueprint("admin_route", __name__)

@bp_admin.route("/admin/map")
@roles_accepted("Admin")
def map():
    return render_template("admin/map.html")

@bp_admin.route("/admin/start_order", methods=["POST"])
@roles_accepted("Admin")
def start_order():
    order_number = request.values.get("order_number")
    if(order_number):
        order = Order.query.filter_by(order_number=order_number).first()
        if(order and order.phase == 1):
            order.phase = 2
            db.session.commit()
            return jsonify(True), 200, {"ContentType": "application/json"}
    return jsonify(False), 400, {"ContentType": "application/json"}

@bp_admin.route("/admin/new_purchase", methods=["POST", "GET"])
@roles_accepted("Admin")
def new_purchase():
    form = PurchaseForm()
    if(request.method == "GET"):
        order_number = request.values.get("order_number", default=None)
        order = Order.query.filter_by(order_number=order_number).first()
        if(order is not None):
            form.order_number.data = order_number
    else:
        hidden_entry = form.products.entries.pop(0)
        if(form.validate_on_submit()):
            order = Order.query.filter_by(order_number=form.order_number.data).first()
            if(order):
                order.phase = 3
                if not order.completed:
                    order.completed = datetime.now()
                purchase = Purchase(order_number=form.order_number.data)
                for entry in form.products.entries:
                    product = Product.query.filter_by(title=entry.data["product"]).first()
                    purchase.products.append(PurchaseProducts(purchase_id=purchase.id, product=product, count=entry.data["amount"]))
                db.session.add(purchase)
                db.session.commit()
                return redirect(url_for(request.args.get("next", "main.home")))

        form.products.entries.insert(0, hidden_entry)
    return render_template("admin/create_purchase.html", form=form)

@bp_admin.route("/admin/register", methods=["GET", "POST"])
@roles_accepted( "Admin", "Developer")
def register():
    form = AdminRegisterForm()
    if(form.validate_on_submit()):
        admin = Admin.create_admin(form.phone_number.data, form.firstname.data, form.lastname.data, form.email.data, form.password.data)
    return render_template("admin/login_register.html", form=form, login=False)

@bp_admin.route("/admin/login", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(phone_number=form.phone_number.data).first()
        login_user(user, remember=True)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("admin_route.home"))
    return render_template("admin/login_register.html", form=form, login=True)

@bp_admin.route("/admin/logout")
@roles_accepted("Admin")
def logout():
    db.session.commit()
    logout_user()
    return redirect(url_for("main.home"))

@bp_admin.route("/admin/home")
@roles_accepted("Admin")
def home():
    region_form = AdminRegionForm(region=current_user.admin.region.id if current_user.admin.region else 0)
    return render_template("admin/home.html", region_form=region_form)

@bp_admin.route("/admin/select_region", methods=["POST"])
@roles_accepted("Admin")
def select_region():
    form = AdminRegionForm()
    if(form.validate_on_submit()):
        if(form.region.data == "0"):
            current_user.admin.region = None
        else:
            region = Region.query.filter_by(id=form.region.data).first()
            if(region):
                current_user.admin.region = region
        db.session.commit()
    return redirect(url_for("admin_route.home"))

@bp_admin.route("/admin/create_campaign", methods=["GET", "POST"])
@roles_accepted("Admin")
def create_campaign():
    form = CreateCampaignForm()
    if(request.method == "POST"):
        hidden_entry = form.products.entries.pop(0)
        if(form.validate_on_submit()):
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

            campaign = Campaign(image=filename, info=form.info.data, terms=form.terms.data, start=start, end=end, delivery=form.delivery.data, per_user=form.per_user.data, per_address=form.per_address.data, amount=form.amount.data)
            for entry in form.products.entries:
                product = Product.query.filter_by(title=entry.data["product"]).first()
                campaign.products.append(CampaignProducts(campaign_id=campaign.id, product=product, amount=entry.data["amount"]))
            db.session.add(campaign)
            db.session.commit()
            return redirect(url_for("admin_route.home"))

        form.products.entries.insert(0, hidden_entry)
    return render_template("admin/create_campaign.html", form=form)
