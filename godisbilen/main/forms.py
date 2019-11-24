from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields.html5 import EmailField
from godisbilen.order_number import OrderNumber
from godisbilen.form_fields import DatalistField

class ContactForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired(message="Detta fält är obligatoriskt.")])
    email = EmailField("Email", validators=[DataRequired()])
    subject = DatalistField("Ämne", datalist=["Angående order", "Fråga"], validators=[DataRequired(message="Detta fält är obligatoriskt.")])
    order_number = StringField("Ordernummer")
    message = TextAreaField("Meddelande", validators=[DataRequired(message="Detta fält är obligatoriskt.")])
    submit = SubmitField("Skicka")

    def validate_order_number(self, order_number):
        if(order_number.data.strip() != ""):
            order_number = OrderNumber.query.filter_by(order_number=order_number.data).first()
            if(not order_number):
                raise ValidationError("Det finns ingen order med detta ordernummer!")