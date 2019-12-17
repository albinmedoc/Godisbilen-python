import json
from sqlalchemy import Column, Integer, String, Boolean, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from geoalchemy2 import Geography
from godisbilen.app import db

admin_regions = db.Table("admin_regions",
    db.Column("admin_id", db.Integer(), db.ForeignKey("admin.user_id")),
    db.Column("region_id", db.Integer(), db.ForeignKey("region.id"))
)

class Region(db.Model):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    locations = relationship("Location", back_populates="region")
    bounds = Column(Geography("POLYGON"))
    admins = relationship("Admin", secondary=admin_regions, back_populates="regions")

    @hybrid_property
    def area(self):
        return db.session.query(func.ST_AREA(Region.bounds)).filter(Region.id == self.id).first()[0]
    
    @area.expression
    def area(cls):
        return cls.bounds.ST_Area()

    @hybrid_property
    def center(self):
        return db.session.scalar(self.bounds.ST_Centroid())
    
    @center.expression
    def center(cls):
        return cls.bounds.ST_Centroid()

    @staticmethod
    def get_bounds(regions:list=None, lat_lng:bool=False, active=None):
        bounds = db.session.query(Region.name, func.ST_AsGeoJSON(Region.bounds))
        if(active is not None):
            bounds = bounds.filter_by(active=active)
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