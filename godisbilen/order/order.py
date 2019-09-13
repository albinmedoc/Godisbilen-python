from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, or_
from sqlalchemy.orm import relationship
from godisbilen.app import db
from .utils import random_order_number
from godisbilen.location.utils import get_time_between

class Order(db.Model):
    __tablename__ = "order"
    order_number = Column(String(20), primary_key=True, default=random_order_number)
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", back_populates="orders")
    user_id = Column(Integer, ForeignKey("person.id"))
    user = relationship("User", back_populates="orders")
    phase = Column(Integer, default=1)
    placed = Column(DateTime, nullable=False, default=datetime.now)

    def queue_position(self):
        if(self.phase > 2):
            return None
        return Order.query.filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).count() + 1
    
    @property
    def estimated_time(self):
        if(self.phase > 2):
            return None
        orders = Order.query.filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).all()
        if(not orders):
            return datetime.now() + timedelta(seconds=300)
        time = 0
        last_location = None
        for order in orders:
            current_location = (order.location.lat, order.location.lng)
            if(last_location):
                time_between = get_time_between(last_location, current_location)
                time = time + time_between
            last_location = current_location
        time = time + get_time_between(last_location, (self.location.lat, self.location.lng))
        #Add stoptime (8min) 
        time = time + (len(orders) * 480)
        return datetime.now() + timedelta(seconds=time)
