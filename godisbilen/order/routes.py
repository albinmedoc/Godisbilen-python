from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from godisbilen.order_number import OrderNumber
from godisbilen.order import Order, OrderForm
from godisbilen.user import roles_accepted
from godisbilen.location import Location
from godisbilen.region import Region
from godisbilen.app import db

bp_order = Blueprint("order", __name__)

@bp_order.route("/order_receipt/<order_number>")
def receipt(order_number):
    order_number = OrderNumber.query.filter_by(number=order_number).first()
    order = Order.query.filter_by(order_number=order_number).first()
    if(not order):
        return "Ordern hittades inte"
    return render_template("order/receipt.html", order=order)

@bp_order.route("/get_orders", methods=["GET", "POST"])
@roles_accepted("Admin")
def get_orders():
    phases = request.values.getlist("phase", type=int)
    all_regions = request.values.get("all_regions", default="false") in ["true", "True"]
    orders = db.session.query(Order)
    if(not all_regions and current_user.admin.regions):
        orders = orders.join(Location).join(Region).filter(Region.id == current_user.admin.region.id)
    if(phases):
        orders = orders.filter(Order.phase.in_(phases))
    orders = orders.order_by(Order.placed).all()
    data = []
    for order in orders:
        data.append(order.json)
    return jsonify(data)
