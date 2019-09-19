from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db

user_location = db.Table("user_location",
    db.Column("user_id", Integer, ForeignKey("person.id"), primary_key=True),
    db.Column("location_id", Integer, ForeignKey("location.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    orders = relationship("Order", back_populates="user")
    locations = relationship("Location", secondary=user_location, back_populates="users")

    @property
    def count_orders(self):
        return len(self.orders)
    
    @property
    def home_adress(self):
        if(not self.locations):
            return None
        return max(set(self.locations), key=self.locations.count)

    def __repr__(self):
        return self.phone_number