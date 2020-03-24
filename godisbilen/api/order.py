from flask import jsonify, abort
from flask_cors import cross_origin
from .auth import auth
from godisbilen.order import Order

@cross_origin()
@auth.login_required
def get_orders():
    orders = Order.query.all()
    temp = []
    for order in orders:
        temp.append(order.json)
    return jsonify(temp)

@cross_origin()
@auth.login_required
def get_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if(order):
        return jsonify(order.json)
    abort(404)

def get_last_order():
    order = Order.query.order_by(Order.placed.desc()).first()
    if(order):
        return jsonify(order.json)
    abort(404)
