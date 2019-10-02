import json
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from godisbilen.app import db

class Region(db.Model):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    locations = relationship("Location", back_populates="region")
    bounds = Column(Geography("POLYGON"))
    admins = relationship("Admin", back_populates="region")

    @staticmethod
    def get_bounds(regions=None, lat_lng=False):
        bounds = db.session.query(Region.name, func.ST_AsGeoJSON(Region.bounds))
        if(regions):
            bounds = bounds.filter(Region.name.in_(regions))
        bounds = bounds.all()
        result = {}
        for bound in bounds:
            result[bound[0]] = json.loads(bound[1])["coordinates"][0]
        if(lat_lng):
            for region, region_bounds in result.items():
                for index, coord in enumerate(region_bounds):
                    result[region][index] = {"lng": coord[0], "lat": coord[1]}
        return result

    def __repr__(self):
        return self.name.capitalize()