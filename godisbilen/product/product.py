from sqlalchemy import Column, Integer, String, select, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from godisbilen.app import db
from godisbilen.purchase.purchase import PurchaseProducts

class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    total = Column(Integer)
    purchases = relationship("PurchaseProducts", back_populates="product")

    @hybrid_property
    def stock(self):
        return self.total - self.sold
    
    @stock.expression
    def stock(cls):
        return select([func.sum(PurchaseProducts.count) - cls.total]).where(PurchaseProducts.product_id==cls.id)
    
    @hybrid_property
    def sold(self):
        temp = 0
        for purchase in self.purchases:
            temp = temp + purchase.count
        return temp

    @sold.expression
    def sold(cls):
        return select([func.sum(PurchaseProducts.count)]).where(PurchaseProducts.product_id==cls.id)

    def __repr__(self):
        return self.title