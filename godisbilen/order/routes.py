from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from godisbilen.order import Order, OrderForm
from godisbilen.user import User
from godisbilen.location import Location
from godisbilen.app import db

bp_order = Blueprint("order", __name__)


@bp_order.route("/order", methods=["GET", "POST"])
def new_order():
    form = OrderForm()
    if(form.validate_on_submit()):
        location = Location.query.filter_by(street_number=form.street_number.data, street=form.street.data, city=form.city.data,
                                            country=form.country.data, postal_code=form.postal_code.data, lat=form.lat.data, lng=form.lng.data).first()
        if(not location):
            location = Location(street_number=form.street_number.data, street=form.street.data, city=form.city.data,
                                country=form.country.data, postal_code=form.postal_code.data, lat=form.lat.data, lng=form.lng.data)
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
def get_orders():
    phases = request.values.getlist("phase", type=int)
    orders = db.session.query(Order)
    if(phases):
        orders = orders.filter(Order.phase.in_(phases))

    orders = orders.order_by(Order.placed).all()
    data = []
    for order in orders:
        temp = {}
        temp["order_number"] = order.order_number
        temp["estimated_time"] = order.estimated_time
        temp["phase"] = order.phase
        temp["queue_position"] = order.queue_position()
        temp["tel"] = order.user.phone_number
        temp["street"] = order.location.street
        temp["street_number"] = order.location.street_number
        temp["lat"] = order.location.lat
        temp["lng"] = order.location.lng
        data.append(temp)
    return jsonify(data)
