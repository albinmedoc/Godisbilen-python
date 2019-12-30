from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from geoalchemy2 import WKTElement
from godisbilen.app import db
from godisbilen.order import Order
from godisbilen.location import Location
from godisbilen.region import Region
from godisbilen.main.utils import shop_open

class OrderForm(FlaskForm):
    search = StringField("Vart ska vi komma?")
    lat = DecimalField(id="lat", widget=HiddenInput())
    lng = DecimalField(id="lng", widget=HiddenInput())

    phone_number = TelField("Telefonnummer", render_kw={
                            "autocomplete": "tel"}, validators=[Length(min=6, max=12), DataRequired("Telefonnummer måste anges")])

    submit = SubmitField("Skicka")

    def validate(self):

        # Check if lat and lng is set
        if(not self.lat.data or not self.lng.data):
            temp = list(self.search.errors)
            temp.append("Var snäll och välj ett alternativ i sökresultatet.")
            self.search.errors = tuple(temp)
            return False

        # Check if shop is open
        if(not shop_open()):
            temp = list(self.search.errors)
            temp.append("Godisbilen har för tillfället stängt.")
            self.search.errors = tuple(temp)
            return False
        
        # Check if outside working area
        if(Region.query.filter_by(active=True).filter(Region.bounds.ST_Intersects(WKTElement("POINT({} {})".format(self.lng.data, self.lat.data)))).first() is None):
            temp = list(self.search.errors)
            temp.append("Addressen är utanför våra leveransområden. Hör av dig till 070-856 03 00 så kan vi se om vi har tid att besöka dig.")
            self.search.errors = tuple(temp)
            return False
        
        #Check if a order is already placed on the address
        location = Location.query.filter_by(lat=self.lat.data, lng=self.lng.data).first()
        if(location is not None and Order.query.filter_by(location=location, completed=None).first() is not None):
            temp = list(self.search.errors)
            temp.append("Det finns redan en aktiv order på denna addressen.")
            self.search.errors = tuple(temp)
            return False
        return True
