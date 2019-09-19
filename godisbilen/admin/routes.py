from flask import Blueprint, render_template, request, jsonify
from godisbilen.app import basic_auth, db
from godisbilen.order import Order
from godisbilen.purchase import PurchaseForm, PurchaseProducts, Purchase
from godisbilen.product import Product

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

@bp_admin.route("/new/purchase", methods=["POST", "GET"])
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
            for entry in form.products.entries:
                purchase = Purchase(order_number=form.order_number.data)
                product=Product.query.filter_by(title=entry.data["product"]).first()
                purchase.products.append(PurchaseProducts(purchase_id=purchase.id, product=product, count=entry.data["count"]))
                db.session.add(purchase)
                db.session.commit()
        form.products.entries.insert(0, hidden_entry)
    return render_template("admin/create_purchase.html", form=form)