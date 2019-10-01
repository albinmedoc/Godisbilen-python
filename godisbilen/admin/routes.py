from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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
    if request.method == "GET":
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
                for entry in form.products.entries:
                    purchase = Purchase(order_number=form.order_number.data)
                    product=Product.query.filter_by(title=entry.data["product"]).first()
                    purchase.products.append(PurchaseProducts(purchase_id=purchase.id, product=product, count=entry.data["count"]))
                    db.session.add(purchase)
                db.session.commit()
                return redirect(url_for(request.args.get("next", "main.home")))

        form.products.entries.insert(0, hidden_entry)
    return render_template("admin/create_purchase.html", form=form)

@bp_admin.route("/admin/register", methods=["GET", "POST"])
#@roles_accepted("Admin", "Developer")
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
        return redirect(url_for("admin_route.home"))
    return render_template("admin/login_register.html", form=form, login=True)

@bp_admin.route("/admin/logout")
@roles_accepted("Admin")
def logout():
    current_user.admin.region = None
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
