from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from godisbilen.app import db
from godisbilen.user.user import user_location

class Location(db.Model):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    street_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, default="sv", nullable=False)
    postal_code = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    orders = relationship("Order", back_populates="location")
    users = relationship("User", secondary=user_location, back_populates="locations")

    def __repr__(self):
        return "<" + self.street + " " + str(self.street_number) + ", " + self.city + ">"