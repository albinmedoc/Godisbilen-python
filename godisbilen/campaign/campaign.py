from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from godisbilen.order_number import OrderNumber
from godisbilen.app import db
from godisbilen.user import User
from godisbilen.location import Location

class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    image = Column(String(100))
    title = Column(String(60))
    info = Column(String(1000))
    terms = Column(String(400))
    start = Column(DateTime)
    end = Column(DateTime)
    delivery = Column(Date)
    per_user = Column(Integer)
    per_address = Column(Integer)
    amount = Column(Integer)
    orders = relationship("CampaignOrder", cascade="all, delete-orphan", back_populates="campaign")

    @hybrid_property
    def count_orders(self):
        return len(self.orders)
    
    @count_orders.expression
    def count_orders(cls):
        return select([func.count(CampaignOrder.id)]).where(CampaignOrder.campaign_id == cls.id).label("count_orders")
                

class CampaignOrder(db.Model):
    __tablename__ = "campaign_order"
    id = Column(Integer, primary_key=True)
    order_number_id = Column(Integer, ForeignKey("order_number.id"), nullable=False)
    order_number = relationship("OrderNumber")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="orders")
    user_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    user = relationship("User", back_populates="campaigns")
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location")
    delivered = Column(DateTime, nullable=True)

    def create(campaign, phone_number, lat, lng):
        order_number = OrderNumber(sufix="C")
        db.session.add(order_number)

        user = User.query.filter_by(phone_number=phone_number).first()
        if(not user):
            user = User(phone_number=phone_number)
            db.session.add(user)

        location = Location.query.filter_by(lat=lat, lng=lng).first()
        if(not location):
            location = Location(lat=lat, lng=lng)
            db.session.add(location)

        campaign_order = CampaignOrder(order_number=order_number, user=user, location=location)
        db.session.commit()
        return campaign_order

        @hybrid_property
        def placed(self):
            return self.order_number.created
        
        @placed.expression
        def placed(cls):
            return select([OrderNumber.created]).where(OrderNumber.id==cls.order_number_id).label("placed")
