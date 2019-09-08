from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from .admin import Admin
from godisbilen.app import bcrypt

class LoginForm(FlaskForm):
    username = StringField("AnvändarID", validators=[DataRequired()])
    password = PasswordField("Lösenord", validators=[DataRequired()])
    submit = SubmitField("Logga in")

    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if(not admin):
            raise ValidationError("Användarnamn finns ej!")
    
    def validate_password(self, password):
        admin = Admin.query.filter_by(username=self.username.data).first()
        if(admin and not bcrypt.check_password_hash(admin.password, password.data)):
            raise ValidationError("Lösenordet matchar inte användarnamnet!")