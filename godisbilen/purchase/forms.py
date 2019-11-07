from wtforms import Form as NoCsrfForm, FieldList
from wtforms.fields import StringField, FormField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, NumberRange, ValidationError
from wtforms.fields.html5 import IntegerField
from flask_wtf import FlaskForm
from godisbilen.form_fields import DatalistField
from godisbilen.product import Product
from godisbilen.order import Order

class ProductForm(NoCsrfForm):
    product = DatalistField("Produkt", validators=[DataRequired(message="Detta fält är obligatoriskt")])
    amount = IntegerField("Antal", validators=[DataRequired(message="Detta fält är obligatoriskt"), NumberRange(min=1, message="Minsta antal är 1")])

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.product.datalist = [p.title for p in Product.query.all()]
    
    def validate_product(self, product):
        product = Product.query.filter_by(title=product.data).first()
        if(not product):
            raise ValidationError("Produkten finns inte inlagd i databasen.")
    
    def validate_amount(self, amount):
        product = Product.query.filter_by(title=self.product.data).first()
        if(product and product.stock < amount.data):
            raise ValidationError("Det ska inte finnas så många i lager, är du säker på att du skrev rätt?")

    def __repr__(self):
        return self.amount + "st " + self.product


class PurchaseForm(FlaskForm):
    order_number = StringField("Ordernummer",validators=[Length(min=20, max=20, message="Måste innehålla exakt 20 tecken.")])
    products = FieldList(FormField(ProductForm), min_entries=2)
    submit = SubmitField("Skapa")

    def validate_order_number(self, order_number):
        order = Order.query.filter_by(order_number=order_number.data).first()
        if(not order):
            raise ValidationError("Det finns ingen order med det ordernummer!")
