from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from godisbilen.app import db
from godisbilen.purchase.purchase import PurchaseProducts

class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    total = Column(Integer)
    purchases = relationship("PurchaseProducts", back_populates="product")

    @property
    def stock(self):
        return self.total - self.sold
    
    @property
    def sold(self):
        temp = 0
        for purchase in self.purchases:
            temp = temp + purchase.count
        return temp

    def __repr__(self):
        return self.title