#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import *
import models
from os import getenv

association_table = Table(
    "place_amenity", Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False)
    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place",
                           cascade="delete")
    amenities = relationship("Amenity",
                             secondary="place_amenity", viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        """for FileStorage"""

        @property
        def reviews(self):
            from models.review import Review
            """ returns the list of Review instances"""
            list_review = []
            for review in models.storage.all(Review).values():
                if review.id == self.id:
                    list_review.append(review)
            return list_review

        @property
        def amenities(self):
            from models.amenity import Amenity
            """ returns the list of Amenity instances based on the attribute
                amenity_ids that contains all Amenity.id linked to the Place"""
            list_amenity = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    list_amenity.append(amenity)
            return list_amenity

        @amenities.setter
        def amenities(self, value):
            from models.amenity import Amenity
            """ handles append method for adding an Amenity.id to the
                attribute amenity_ids list. This method should accept only
                Amenity object"""
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
