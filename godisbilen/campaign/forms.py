from datetime import time
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, HiddenField, FormField, FieldList, SubmitField
from wtforms.fields.html5 import TelField, IntegerField, DecimalField, DateField, TimeField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Length, Optional
from geoalchemy2 import WKTElement
from godisbilen.campaign import Campaign, CampaignOrder
from godisbilen.user import User
from godisbilen.location import Location
from godisbilen.region import Region

class JoinCampaignForm(FlaskForm):
    campaign_id = HiddenField()
    search = StringField("Vart ska vi komma?")
    lat = DecimalField(id="lat", widget=HiddenInput(), validators=[
                       DataRequired(message="Kunde inte hitta lat koordinat")])
    lng = DecimalField(id="lng", widget=HiddenInput(), validators=[
                       DataRequired(message="Kunde inte hitta lng koordinat")])

    phone_number = TelField("Telefonnummer", render_kw={
                            "autocomplete": "tel"}, validators=[DataRequired("Telefonnummer måste anges")])

    submit = SubmitField("Skicka")

    def validate(self):
        campaign = Campaign.query.filter_by(id=self.campaign_id.data).first()
        if(not campaign):
            temp = list(self.search.errors)
            temp.append("Något gick snett. Försök igen.")
            self.search.errors = tuple(temp)
            return False

        inside = Region.query.filter(Region.bounds.ST_Intersects(WKTElement("POINT({} {})".format(self.lng.data, self.lat.data)))).first()
        if(not inside):
            temp = list(self.search.errors)
            temp.append("Addressen är utanför våra leveransområden")
            self.search.errors = tuple(temp)
            return False
        user = User.query.filter_by(phone_number=self.phone_number.data).first()
        if(user):
            user_order_count = CampaignOrder.query.filter_by(user=user).count()
            if(campaign.per_user and user_order_count >= campaign.per_user):
                temp = list(self.phone_number.errors)
                temp.append("Du har nått maxantalet ordrar för detta erbjudande (" + str(campaign.per_user) + "st).")
                self.phone_number.errors = tuple(temp)
                return False

        location = Location.query.filter_by(lat=self.lat.data, lng=self.lng.data).first()
        if(location):
            location_order_count = CampaignOrder.query.filter_by(location=location).count()
            if(campaign.per_address and location_order_count >= campaign.per_address):
                temp = list(self.search.errors)
                temp.append("Adressen har nått maxantalet ordrar för detta erbjudande (" + str(campaign.per_address) + "st).")
                self.search.errors = tuple(temp)
                return False
        return True

class CreateEditCampaignForm(FlaskForm):
    image = FileField("Bild", validators=[FileRequired(message="Du måste välja en bild.")])
    title = StringField("Titel", validators=[DataRequired("Detta fält är obligatorisk."), Length(max=60, message="Max %(max)d tecken.")])
    info = StringField("Extra information", validators=[Length(max=1000, message="Max %(max)d tecken.")])
    terms = StringField("Villkor", validators=[Length(max=400, message="Max %(max)d tecken.")])
    start_date = DateField("Börjar (datum)", validators=[DataRequired("Detta fält är obligatorisk.")])
    start_time = TimeField("Börjar (tid)", default=time(), validators=[DataRequired("Detta fält är obligatorisk.")])
    end_date = DateField("Avslutas (datum)", validators=[DataRequired("Detta fält är obligatorisk.")])
    end_time = TimeField("Avslutas (tid)", default=time(23, 59), validators=[DataRequired("Detta fält är obligatorisk.")])
    delivery = DateField("Levereras", validators=[DataRequired("Detta fält är obligatorisk.")])
    per_user = IntegerField("Max per telefonnummer", validators=[Optional()])
    per_address = IntegerField("Max per adress", validators=[Optional()])
    amount = IntegerField("Antal erbjudande", validators=[Optional()])
    submit = SubmitField("Skapa")
