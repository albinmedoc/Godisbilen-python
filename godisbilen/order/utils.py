import string
import random
from datetime import datetime

def random_order_number():
    from .order import Order
    prefix = str(datetime.today().year) + "-"
    order_number = "".join(random.choice(string.ascii_uppercase) for x in range(15))
    while(Order.query.filter_by(order_number=order_number).first()):
        order_number = "".join(random.choice(string.ascii_uppercase) for x in range(15))
    return prefix + order_number
