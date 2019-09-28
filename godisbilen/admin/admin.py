from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from godisbilen.app import db, bcrypt
from godisbilen.user import User

admin_regions = db.Table("admin_regions",
    db.Column("admin_id", db.Integer(), db.ForeignKey("admin.user_id", ondelete="CASCADE")),
    db.Column("region_id", db.Integer(), db.ForeignKey("region.id", ondelete="CASCADE"))
)

class Admin(db.Model):
    user_id = Column(Integer, ForeignKey("person.id"), primary_key=True)
    user = relationship("User", back_populates="admin")
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(60))
    password = db.Column(db.String(60))
    regions = db.relationship("Region", secondary=admin_regions, back_populates="admins")

    def clear_regions(self):
        self.regions[:] = []
        db.session.commit()

    def __repr__(self):
        return "Admin(" + self.firstname + " " + self.lastname + ")"

    
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
