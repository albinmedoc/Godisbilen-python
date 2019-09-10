from flask import Blueprint, render_template, request, jsonify
from godisbilen.app import basic_auth, db
from godisbilen.order import Order

bp_admin = Blueprint("admin_route", __name__)

@bp_admin.route("/admin/map")
@basic_auth.required
def test():
    return render_template("admin/map.html")

@bp_admin.route("/admin/start_order", methods=["POST"])
@basic_auth.required
def start_order():
    order_number = request.values.get("order_number")
    if(order_number):
        order = Order.query.filter_by(order_number=order_number).first()
        if(order and order.phase == 1):
            order.phase = 2
            db.session.commit()
            return jsonify(True), 200, {"ContentType": "application/json"}
    return jsonify(False), 400, {"ContentType": "application/json"}

@bp_admin.route("/admin/end_order", methods=["POST"])
@basic_auth.required
def end_order():
    order_number = request.values.get("order_number")
    if(order_number):
        order = Order.query.filter_by(order_number=order_number).first()
        if(order and order.phase == 2):
            order.phase = 3
            db.session.commit()
            return jsonify(True), 200, {"ContentType": "application/json"}
    return jsonify(False), 400, {"ContentType": "application/json"}