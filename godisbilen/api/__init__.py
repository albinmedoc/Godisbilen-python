from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

from .order import get_orders, get_order, get_last_order
bp_api.add_url_rule("/orders", "orders", get_orders)
bp_api.add_url_rule("/orders/<order_id>", "order", get_order)
bp_api.add_url_rule("/orders/last", "last_order", get_last_order)

from .region import get_regions, get_region
bp_api.add_url_rule("/regions", "regions", get_regions)
bp_api.add_url_rule("/regions/<region_name>", "region", get_region)
