import re
from datetime import datetime, timedelta
from flask_mail import Message
from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, or_, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from godisbilen.app import db, mail
from godisbilen.main.utils import send_sms
from godisbilen.order_number import OrderNumber
from godisbilen.user import User
from godisbilen.location import Location
from godisbilen.region import Region

class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    order_number_id = Column(Integer, ForeignKey("order_number.id"), nullable=False)
    order_number = relationship("OrderNumber")
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location", back_populates="orders")
    user_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    phase = Column(Integer, default=1)
    estimated_delivery = Column(DateTime, nullable=True)
    completed = Column(DateTime, nullable=True)
    
    @staticmethod
    def create(phone_number, lat, lng):
        # Delete all non-numeric characters
        phone_number = re.sub("[^0-9]", "", phone_number)

        # get user, create if none exists
        user = User.query.filter_by(phone_number=phone_number).first()
        if(not user):
            user = User(phone_number=phone_number)
            db.session.add(user)
        
        # Get a place, create if it doesn't exist
        location = Location.query.filter_by(lat=lat, lng=lng).first()
        if(not location):
            location = Location(lat=lat, lng=lng)
            db.session.add(location)
        db.session.commit()

        # Get the current time
        now = datetime.now()

        # Get the latest order that is active in the current region
        last_active_order = Order.query.join(Location).join(Region).filter(Region.id == location.region.id).filter(Order.placed < now).filter(or_(Order.phase == 1, Order.phase == 2)).order_by(Order.placed.desc()).first()
        
        # Check if an order was found
        if(last_active_order is not None):
            # Calculate the time between the last active order and the current order
            time_between = last_active_order.location.time_between(location)

            # Add time between locations and stop time to the last active order's estimated delivery time
            estimated_delivery = last_active_order.estimated_delivery + timedelta(seconds=time_between + current_app.config["STOP_TIME"])

        else:
            # Calculate the time between the starting point and the current order
            time_between = location.time_between(current_app.config["START_LOC"])

            # Add time between locations and start time to the current time
            estimated_delivery = now + timedelta(seconds=time_between + current_app.config["START_TIME"])

        # Create order and add to database
        order = Order(order_number=OrderNumber(sufix="O"), location=location, user=user, estimated_delivery=estimated_delivery)
        db.session.add(order)
        db.session.commit()

        # Send sms to admins assigned to the region
        url = "https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=" + str(lat) + "," + str(lng)
        message = "Ny order från " + user.phone_number + " på adressen: " + location.formatted_address + ". Beräknad leverans: " + estimated_delivery.time().strftime("%H:%M") + " \n " + url
        # recipients = [admin.user.phone_number for admin in location.region.admins] + current_app.config["INCLUDE_PHONE_NUMBER_ORDER"]
        recipients = current_app.config["INCLUDE_PHONE_NUMBER_ORDER"]
        for phone_number in recipients:
            send_sms(message, phone_number)

        return order
    
    @hybrid_property
    def placed(self):
        return self.order_number.created
    
    @placed.expression
    def placed(cls):
        return select([OrderNumber.created]).where(OrderNumber.id==cls.order_number_id).label("placed")

    @property
    def queue_position(self):
        if(self.phase > 2):
            return None
        return Order.query.join(Location).join(Region).filter(Region.id == self.location.region.id).filter(Order.placed < self.placed).filter(or_(Order.phase == 1, Order.phase == 2)).count() + 1
    
    @property
    def status(self):
        if(self.phase == 1):
            return "Köande"
        elif(self.phase == 2):
            return "Pågående"
        elif(self.phase == 3):
            return "Färdig"
        else:
            return None

    @property
    def json(self):
        temp =  {}
        temp["order_number"] = self.order_number.number
        temp["estimated_delivery"] = str(self.estimated_delivery)
        temp["phase"] = self.phase
        temp["queue_position"] = self.queue_position
        temp["tel"] = self.user.phone_number
        temp["formatted_address"] = self.location.formatted_address
        temp["street"] = self.location.street_name
        temp["street_number"] = self.location.street_number
        temp["lat"] = self.location.lat
        temp["lng"] = self.location.lng
        return temp

    def __repr__(self):
        return self.order_number.number
