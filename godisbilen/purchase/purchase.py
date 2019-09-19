from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db

class PurchaseProducts(db.Model):
    __tablename__ = "purchase_products"
    purchase_id = Column(String(20), ForeignKey("purchase.id"), primary_key=True)
    purchase = relationship("Purchase", back_populates="products")
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    product = relationship("Product", back_populates="purchases")
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return str(self.count) + "st " +  self.product.title

class Purchase(db.Model):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True)
    order_number = Column(String(20), ForeignKey("order.order_number"))
    order = relationship("Order", back_populates="purchase")
    products = relationship("PurchaseProducts", cascade="all, delete-orphan", back_populates="purchase")

    @property
    def count_products(self):
        temp = 0
        for product in self.products:
            temp = temp + product.count
        return temp

    @property
    def user(self):
        return self.order.user
