from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DecimalField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from shapely.geometry import Point, Polygon
from godisbilen.main.utils import shop_open
from godisbilen.location.utils import get_city_boundaries


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

        # Check if inside working areas
        lat = self.lat.data
        lng = self.lng.data
        point = Point(lat, lng)
        city_boundaries = get_city_boundaries()

        inside = False
        for city in city_boundaries:
            city_boundary = []
            for coord in city_boundaries[city]:
                city_boundary.append((coord["lat"], coord["lng"]))
            city_boundary = Polygon(city_boundary)
            if(city_boundary.contains(point)):
                inside = True
        if(not inside):
            temp = list(self.full_adress.errors)
            temp.append("Addressen är utanför våra leveransområden")
            self.full_adress.errors = tuple(temp)
            return False
        return True

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
