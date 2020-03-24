import string
from random import choices
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from godisbilen.app import db

class ShortUrl(db.Model):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    visits = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        characters = string.digits + string.ascii_lowercase

        # Generate until short_url is unique
        short_url = "".join(choices(characters, k=4))
        while(self.query.filter_by(short_url=short_url).first() is not None):
            short_url = "".join(choices(characters, k=4))
        self.short_url = short_url
