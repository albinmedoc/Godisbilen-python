from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DecimalField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from sqlalchemy import func
from geoalchemy2 import WKTElement
from godisbilen.app import db
from godisbilen.region import Region
from godisbilen.main.utils import shop_open

class OrderForm(FlaskForm):
    search = StringField("Vart ska vi komma?")
    lat = DecimalField(id="lat", widget=HiddenInput(), validators=[
                       DataRequired(message="Kunde inte hitta lat koordinat")])
    lng = DecimalField(id="lng", widget=HiddenInput(), validators=[
                       DataRequired(message="Kunde inte hitta lng koordinat")])

    phone_number = TelField("Telefonnummer", render_kw={
                            "autocomplete": "tel"}, validators=[DataRequired("Telefonnummer måste anges")])

    submit = SubmitField("Skicka")

    def validate(self):
        # Check if shop is open
        if(not shop_open()):
            temp = list(self.search.errors)
            temp.append("Godisbilen har för tillfället stängt")
            self.search.errors = tuple(temp)
            return False
        
        inside = Region.query.filter(Region.bounds.ST_Intersects(WKTElement("POINT({} {})".format(self.lng.data, self.lat.data)))).first()
        if(not inside):
            temp = list(self.search.errors)
            temp.append("Addressen är utanför våra leveransområden")
            self.search.errors = tuple(temp)
            return False
        return True
