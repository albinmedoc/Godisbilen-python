from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from godisbilen.app import db
from godisbilen.purchase.purchase import purchase_products

class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    stock = Column(Integer, unique=True)
    purchases = relationship("Purchase", secondary=purchase_products, back_populates="products")

    def __repr__(self):
        return self.title