from datetime import datetime
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
    buyers = relationship("CampaignUsers", cascade="all, delete-orphan", back_populates="campaign")

class CampaignUsers(db.Model):
    __tablename__ = "campaign_users"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="buyers")
    user_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    user = relationship("User", back_populates="campaigns")
    placed = Column(DateTime, nullable=False, default=datetime.now)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    location = relationship("Location")