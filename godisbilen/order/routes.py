from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from godisbilen.order import Order, OrderForm
from godisbilen.user import User, roles_accepted
from godisbilen.location import Location
from godisbilen.region import Region
from godisbilen.app import db

bp_order = Blueprint("order", __name__)


@bp_order.route("/order", methods=["GET", "POST"])
def new_order():
    form = OrderForm()
    if(form.validate_on_submit()):
        location = Location.query.filter_by(lat=form.lat.data, lng=form.lng.data).first()
        if(not location):
            location = Location(lat=form.lat.data, lng=form.lng.data)
            db.session.add(location)
        user = User.query.filter_by(
            phone_number=form.phone_number.data).first()
        if(not user):
            user = User(phone_number=form.phone_number.data)
            db.session.add(user)
        order = Order(location=location, user=user)
        db.session.add(order)
        if(location not in user.locations):
            user.locations.append(location)
        db.session.commit()
        return redirect(url_for("order.order_confirmation", order_number=order.order_number))
    return render_template("order/order.html", form=form)

@bp_order.route("/order_confirmation/<order_number>")
def order_confirmation(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if(not order):
        return "Ordern hittades inte"
    return render_template("order/order_confirmation.html", order=order)

@bp_order.route("/get_orders", methods=["GET", "POST"])
@roles_accepted("Admin")
def get_orders():
    phases = request.values.getlist("phase", type=int)
    orders = db.session.query(Order)
    if(True):
        orders = orders.join(Location).join(Region).filter(Region.id.in_([region.id for region in current_user.admin.regions]))
    if(phases):
        orders = orders.filter(Order.phase.in_(phases))
    orders = orders.order_by(Order.placed).all()
    data = []
    for order in orders:
        data.append(order.json)
    return jsonify(data)
