from flask_wtf import FlaskForm
from wtforms import Form as NoCsrfForm, FieldList
from wtforms import StringField, PasswordField, FormField, BooleanField, SubmitField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user
from godisbilen.app import bcrypt
from godisbilen.user import User
from godisbilen.admin import Admin
from godisbilen.region import Region

class AdminLoginForm(FlaskForm):
    phone_number = TelField("Telefonnummer", validators=[DataRequired()])
    password = PasswordField("Lösenord", validators=[DataRequired()])
    submit = SubmitField("Logga in")

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if(user is None):
            raise ValidationError("Det finns inget konto med det telefonnummret.")
        elif(not user.has_roles("Admin")):
            raise ValidationError("Du har inte rättigheter till att logga in.")

    def validate_password(self, password):
        user = User.query.filter_by(phone_number=self.phone_number.data).first()
        if(user and user.has_roles("Admin")):
            if(not bcrypt.check_password_hash(user.admin.password, password.data)):
                raise ValidationError("Lösenordet matchar inte telefonnummret.")

class AdminRegisterForm(FlaskForm):
    phone_number = TelField("Telefonnummer", validators=[DataRequired()])
    firstname = StringField("Förnamn", validators=[DataRequired()])
    lastname = StringField("Förnamn", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Lösenord", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Bekräfta lösenord", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Skapa")

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if(user and user.has_roles("Admin")):
            raise ValidationError("Det finns redan ett Admin-konto med detta telefonnummer.")
    
    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if(admin):
            raise ValidationError("Det finns redan ett Admin-konto med denna emailen.")

class AdminRegionForm(FlaskForm):
    submit = SubmitField("Spara")

    def __init__(self, *args, **kwargs):
        super(AdminRegionForm, self).__init__(*args, **kwargs)
        regions = Region.query.all()
        if(regions):
            for region in regions:
                selected = region in current_user.admin.regions
                setattr(AdminRegionForm, region.name, BooleanField(region.name, default=selected))


