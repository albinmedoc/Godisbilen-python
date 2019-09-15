from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields.html5 import EmailField
from godisbilen.order import Order
from godisbilen.form_fields import DatalistField

class ContactForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    subject = DatalistField("Ämne", datalist=["Angående order", "Fråga"], validators=[DataRequired()])
    order_number = StringField("Ordernummer")
    message = TextAreaField("Meddelande", validators=[DataRequired()])
    submit = SubmitField("Skicka")

    def validate_order_number(self, order_number):
        if(order_number.data.strip() != ""):
            order = Order.query.filter_by(order_number=order_number.data).first()
            if(not order):
                raise ValidationError("Det finns ingen order med detta ordernummer!")