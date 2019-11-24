import random
from datetime import datetime
from string import ascii_uppercase
from sqlalchemy import Column, Integer, String, DateTime
from godisbilen.app import db

class OrderNumber(db.Model):
    __tablename__ = "order_number"
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, prefix=str(datetime.today().year), sufix=""):
        random_length = 20 - (len(prefix) + len(sufix))
        number = "".join(random.choice(ascii_uppercase) for x in range(random_length))
        while(OrderNumber.query.filter_by(number=number).first()):
            number = "".join(random.choice(ascii_uppercase) for x in range(random_length))
        number = prefix + number + sufix
        self.number = number

    def __repr__(self):
        return self.number
    