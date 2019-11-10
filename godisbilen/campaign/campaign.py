from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db

class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    image = Column(String(100))
    info = Column(String(1000))
    terms = Column(String(400))
    start = Column(DateTime)
    end = Column(DateTime)
    delivery = Column(Date)
    per_user = Column(Integer)
    per_address = Column(Integer)
    amount = Column(Integer)
    products = relationship("CampaignProducts", cascade="all, delete-orphan", back_populates="campaign")
    buyers = relationship("CampaignUsers", cascade="all, delete-orphan", back_populates="campaign")

class CampaignProducts(db.Model):
    __tablename__ = "campaign_products"
    campaign_id = Column(Integer, ForeignKey("campaign.id"), primary_key=True)
    campaign = relationship("Campaign", back_populates="products")
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    product = relationship("Product")
    amount = Column(Integer, default=1)

class CampaignUsers(db.Model):
    __tablename__ = "campaign_users"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="buyers")
    user_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    user = relationship("User", back_populates="campaigns")
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location")