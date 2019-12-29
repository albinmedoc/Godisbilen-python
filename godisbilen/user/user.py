from sqlalchemy import Column, Integer, String, Float, ForeignKey, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from godisbilen.app import db, login
from godisbilen.user.role import Role
from godisbilen.location import Location

user_roles = db.Table("user_roles",
    db.Column("user_id", db.Integer(), db.ForeignKey("person.id", ondelete="CASCADE")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))
)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    orders = relationship("Order", back_populates="user")
    roles = db.relationship("Role", secondary=user_roles, backref="users")
    admin = relationship("Admin", uselist=False, back_populates="user")

    @property
    def locations(self):
        # No duplicates
        return list(dict.fromkeys([order.location for order in self.orders]))

    @hybrid_property
    def count_orders(self):
        return len(self.orders)
    
    @count_orders.expression
    def count_orders(cls):
        from godisbilen.order import Order
        return select([func.count(Order.id)]).where(Order.user_id == cls.id).label("count_orders")
    
    @property
    def home_adress(self):
        if(not self.locations):
            return None
        return max(set(self.locations), key=self.locations.count)
    
    def has_roles(self, *requirements):
        role_names = [role.name for role in self.roles]
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True
    
    def add_role(self, role):
        if(role not in [(role.name) for role in self.roles]):
            role_object = Role.query.filter_by(name=role).first()
            if(role_object is None):
                role_object = Role(name=role)
            self.roles.append(role_object)
            db.session.commit()

    def __repr__(self):
        return self.phone_number