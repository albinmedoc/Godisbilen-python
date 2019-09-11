from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import TextInput, HTMLString
from wtforms.fields.html5 import EmailField
from godisbilen.order import Order

class DatalistInput(TextInput):
    """
    Custom widget to create an input with a datalist attribute
    """

    def __init__(self, datalist=""):
        super(DatalistInput, self).__init__()
        self.datalist = datalist

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        html = [u'<datalist id="{}_list">'.format(field.id)]

        for item in field.datalist:
            html.append(u'<option value="{}">'.format(item))

        html.append(u'</datalist>')
        if(field.data is None):
            field.data = ""

        html.append(u'<input list="{}_list" id="{}" name="{}" value="{}" placeholder=" ">'.format(field.id, field.id, field.name, field.data))

        return HTMLString(u''.join(html))


class DatalistField(StringField):
    """
    Custom field type for datalist input
    """
    widget = DatalistInput()

    def __init__(self, label=None, datalist="", validators=None, **kwargs):
        super(DatalistField, self).__init__(label, validators, **kwargs)
        self.datalist = datalist

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''

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