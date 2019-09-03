from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db

user_roles = db.Table("user_roles",
    db.Column("user_id", db.Integer(), db.ForeignKey("person.id", ondelete="CASCADE")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))
)

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
    roles = db.relationship("Role", secondary=user_roles, backref="users")

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
                    return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in role_names:
                    return False
        # All requirements have been met: return True
        return True
    
    def add_role(self, role):
        if(role not in [(role.name) for role in self.roles]):
            role_object = Role.query.filter_by(name=role).first()
            if(role_object is None):
                role_object = Role(name=role)
            self.roles.append(role_object)
            db.session.commit()

    def get_home_adress(self):
        if(not self.locations):
            return None
        return max(set(self.locations), key=self.locations.count)