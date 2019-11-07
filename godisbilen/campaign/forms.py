from datetime import time
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, HiddenField, FormField, FieldList, SubmitField
from wtforms.fields.html5 import TelField, IntegerField, DecimalField, DateField, TimeField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Length, Optional
from geoalchemy2 import WKTElement
from godisbilen.campaign import Campaign, CampaignUsers
from godisbilen.location import Location
from godisbilen.region import Region
from godisbilen.purchase.forms import ProductForm

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
        user_order_count = CampaignUsers.query.filter_by(user_id=current_user.id).count()
        if(campaign.per_user and user_order_count >= campaign.per_user):
            return False
        return True

class CreateCampaignForm(FlaskForm):
    image = FileField("Bild")
    info = StringField("Extra information", validators=[Length(max=1000, message="Max %(max)d tecken")])
    terms = StringField("Villkor", validators=[Length(max=400, message="Max %(max)d tecken")])
    start_date = DateField("Börjar (datum)", validators=[DataRequired("Detta fält är obligatorisk.")])
    start_time = TimeField("Börjar (tid)", default=time(), validators=[DataRequired("Detta fält är obligatorisk.")])
    end_date = DateField("Avslutas (datum)", validators=[DataRequired("Detta fält är obligatorisk.")])
    end_time = TimeField("Avslutas (tid)", default=time(23, 59), validators=[DataRequired("Detta fält är obligatorisk.")])
    delivery = DateField("Levereras", validators=[DataRequired("Detta fält är obligatorisk.")])
    per_user = IntegerField("Max per telefonnummer", validators=[Optional()])
    per_address = IntegerField("Max per adress (Fungerar ej)", validators=[Optional()])
    amount = IntegerField("Antal erbjudande", validators=[Optional()])
    products = FieldList(FormField(ProductForm), min_entries=1)
    submit = SubmitField("Skapa")
