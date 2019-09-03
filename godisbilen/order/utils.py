import string
import random

def random_order_number():
    from .order import Order
    order_number = "".join(random.choice(string.ascii_uppercase) for x in range(20))
    while(Order.query.filter_by(order_number=order_number).first()):
        order_number = "".join(random.choice(string.ascii_uppercase) for x in range(20))
    return order_number
