from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
from geoalchemy2 import WKTElement
from godisbilen.order import Order
from godisbilen.location import Location
from godisbilen.region import Region
from godisbilen.main.utils import shop_open
from godisbilen.form.validators import PhoneNumber

class OrderForm(FlaskForm):
    search = StringField("Vart ska vi komma?")
    lat = DecimalField(id="lat", widget=HiddenInput())
    lng = DecimalField(id="lng", widget=HiddenInput())

    phone_number = StringField("Telefonnummer", render_kw={
                            "autocomplete": "tel"}, validators=[DataRequired("Telefonnummer måste anges"), PhoneNumber(r"[\d]{8,10}", "Inget giltigt telefonnummer. Skall innehålla 8-10 siffror.")])

    submit = SubmitField("Skicka")

    def validate_search(self, search):
        # Check if lat and lng is set
        if(not self.lat.data or not self.lng.data):
            raise ValidationError("Var snäll och välj ett alternativ i sökresultatet.")

        # Check if shop is open
        if(not shop_open()):
            raise ValidationError("Godisbilen har för tillfället stängt.")

        # Check if outside working area
        if(Region.query.filter_by(active=True).filter(Region.bounds.ST_Intersects(WKTElement("POINT({} {})".format(self.lng.data, self.lat.data)))).first() is None):
            raise ValidationError("Addressen är utanför våra leveransområden. Hör av dig till 070-856 03 00 så kan vi se om vi har tid att besöka dig.")
        
        # Check if a order is already placed on the address
        location = Location.query.filter_by(lat=self.lat.data, lng=self.lng.data).first()
        if(location is not None and Order.query.filter_by(location=location, completed=None).first() is not None):
            raise ValidationError("Det finns redan en aktiv order på denna addressen.")
