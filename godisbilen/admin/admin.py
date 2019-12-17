from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db, bcrypt
from godisbilen.user import User
from godisbilen.region.region import admin_regions

class Admin(db.Model):
    """
    A class used to represent an Admin

    Attributes
    ----------
    user_id: int
        The user_id of the admin
    user: User
        The user object of the admin
    firstname: str
        The admins firstname
    lastname: str
        The admins lastname
    email: str
        The admins email
    password: str
        The admins hashed password
    regions: list<Region>
        A list of regions assigned to the admin

    Methods
    -------
    __repr__()
        Returns a representation of the admin in a str-format
    """
    user_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    user = relationship("User", back_populates="admin")
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String(60))
    password = Column(String(60))
    regions = relationship("Region", secondary=admin_regions, back_populates="admins")

    def __repr__(self):
        return self.firstname + " " + self.lastname

    
    @staticmethod
    def create_admin(phone_number, firstname, lastname, email, password):
        user = User.query.filter_by(phone_number=phone_number).first()
        if(not user):
            user = User(phone_number=phone_number)
            db.session.add(user)

        admin = Admin.query.filter_by(user=user).first()
        if(not admin):
            if(not user.has_roles("Admin")):
                user.add_role("Admin")
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            admin = Admin(user=user, firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        return admin
