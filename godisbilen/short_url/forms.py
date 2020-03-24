from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import URLField

class ShortURLForm(FlaskForm):
    original_url = URLField("Dirigera till", validators=[DataRequired("Detta fält är obligatoriskt.")])
    submit = SubmitField("Skapa kort URL")
    