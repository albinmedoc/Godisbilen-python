from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, or_
from sqlalchemy.orm import relationship
from godisbilen.app import db
from godisbilen.location import Location
from godisbilen.region import Region
from .utils import random_order_number

class Order(db.Model):
    __tablename__ = "order"
    order_number = Column(String(20), primary_key=True, default=random_order_number)
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", back_populates="orders")
    user_id = Column(Integer, ForeignKey("person.id"))
    user = relationship("User", back_populates="orders")
    phase = Column(Integer, default=1)
    placed = Column(DateTime, nullable=False, default=datetime.now)
    completed = Column(DateTime, nullable=True)
    purchase = relationship("Purchase", uselist=False, back_populates="order")

    @property
    def queue_position(self):
        if(self.phase > 2):
            return None
        return Order.query.join(Location).join(Region).filter(Region.id == self.location.region.id).filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).count() + 1
    
    @property
    def estimated_delivery(self):
        if(self.phase > 2):
            return None
        orders = Order.query.join(Location).join(Region).filter(Region.id == self.location.region.id).filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).all()
        if(not orders):
            return datetime.now() + timedelta(seconds=300)
        orders.append(self)
        time = 0
        last_location = None
        for location in [order.location for order in orders]:
            if(last_location):
                time = time + last_location.time_between(location)
            last_location = location
        #Add stoptime (8min) 
        time = time + ((len(orders) - 1) * 480)
        return datetime.now() + timedelta(seconds=time)
    
    @property
    def status(self):
        if(self.phase == 1):
            return "Queueing"
        elif(self.phase == 2):
            return "On going"
        elif(self.phase == 3):
            return "Completed"
        else:
            return None
    
    def __repr__(self):
        return self.order_number

    @property
    def json(self):
        temp =  {}
        temp["order_number"] = self.order_number
        temp["estimated_delivery"] = self.estimated_delivery
        temp["phase"] = self.phase
        temp["queue_position"] = self.queue_position
        temp["tel"] = self.user.phone_number
        temp["street"] = self.location.street_name
        temp["street_number"] = self.location.street_number
        temp["lat"] = self.location.lat
        temp["lng"] = self.location.lng
        return temp
