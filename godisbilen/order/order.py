from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, or_
from sqlalchemy.orm import relationship
from godisbilen.app import db
from godisbilen.user import User
from godisbilen.location import Location
from godisbilen.region import Region
from .utils import random_order_number

class Order(db.Model):
    __tablename__ = "order"
    order_number = Column(String(20), primary_key=True, default=random_order_number)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location", back_populates="orders")
    user_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    phase = Column(Integer, default=1)
    placed = Column(DateTime, nullable=False, default=datetime.now)
    estimated_delivery = Column(DateTime, nullable=True)
    completed = Column(DateTime, nullable=True)
    purchase = relationship("Purchase", uselist=False, back_populates="order")
    
    @staticmethod
    def create(phone_number, lat, lng):
        user = User.query.filter_by(phone_number=phone_number).first()
        if(not user):
            user = User(phone_number=phone_number)
            db.session.add(user)
        location = Location.query.filter_by(lat=lat, lng=lng).first()
        if(not location):
            location = Location(lat=lat, lng=lng)
            db.session.add(location)
        db.session.commit()

        now = datetime.now()
        orders = Order.query.join(Location).join(Region).filter(Region.id == location.region.id).filter(Order.placed < now).filter(or_(Order.phase == 1, Order.phase == 2)).all()
        # Adding current order location to list
        locations = [order.location for order in orders] + [location]

        # Should start at region center to first location + startup
        time = 240 + locations[0].time_between([db.session.scalar(location.region.center.ST_Y()), db.session.scalar(location.region.center.ST_X())])
        last_location = None
        for _location in locations:
            if(last_location):
                time = time + last_location.time_between(_location)
            last_location = _location
        # Add stoptime (8min) 
        time = time + len(orders) * current_app.config["STOP_TIME"]
        estimated_delivery = now + timedelta(seconds=time)
        order = Order(location=location, user=user, estimated_delivery=estimated_delivery, placed=now)
        return order

    @property
    def queue_position(self):
        if(self.phase > 2):
            return None
        return Order.query.join(Location).join(Region).filter(Region.id == self.location.region.id).filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).count() + 1
    
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

    def __repr__(self):
        return self.order_number
