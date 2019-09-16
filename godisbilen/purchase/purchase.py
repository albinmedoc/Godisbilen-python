from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from godisbilen.app import db

purchase_products = db.Table("purchase_products",
    Column("purchase_id", Integer, ForeignKey("purchase.id")),
    Column("product_id", Integer, ForeignKey("product.id"))
)

class Purchase(db.Model):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("person.id"))
    user = relationship("User", back_populates="purchases")
    products = relationship("Product", secondary=purchase_products, back_populates="purchases", lazy="joined")

    @hybrid_property
    def count_products(self):
        return len(self.products)

    @count_products.expression
    def count_products(cls):
        return db.select([db.func.count(purchase_products.c.product_id)]).where(purchase_products.c.purchase_id == cls.id)
