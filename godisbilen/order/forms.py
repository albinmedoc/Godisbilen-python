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
    full_adress = StringField("Vart ska vi komma?")
    street_number = HiddenField(id="street_number", validators=[
                                DataRequired(message="Gatunummer saknas")])
    street = HiddenField(id="route", validators=[
                         DataRequired(message="Gata saknas")])
    city = HiddenField(id="postal_town", validators=[
                       DataRequired(message="Stad saknas")])
    country = HiddenField(id="country", validators=[
                          DataRequired(message="Land saknas")])
    postal_code = HiddenField(id="postal_code", validators=[
                              DataRequired(message="Postnummer saknas")])
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
            temp = list(self.full_adress.errors)
            temp.append("Godisbilen har för tillfället stängt")
            self.full_adress.errors = tuple(temp)
            return False
        
        inside = Region.query.filter(Region.bounds.ST_Intersects(WKTElement("POINT({} {})".format(self.lng.data, self.lat.data)))).first()
        if(not inside):
            temp = list(self.full_adress.errors)
            temp.append("Addressen är utanför våra leveransområden")
            self.full_adress.errors = tuple(temp)
            return False
        return True
