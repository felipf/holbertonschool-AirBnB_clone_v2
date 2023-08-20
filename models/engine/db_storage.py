#!/usr/bin/python3
"""DBStorage engine defined"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """database storage engine"""

    __engine = None
    __session = None

    def __init__(self, ):
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"), getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"), getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop(self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session)
            all objects depending of the class name"""
        all_classes = [State, City, User, Place, Review, Amenity]

        if cls is None:
            objects = []
            for c in all_classes:
                objects.extend(self.__session.query(c).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            if cls in all_classes:
                objects = self.__session.query(cls)

        result = {}
        for o in objects:
            k = "{}.{}".format(type(o).__name__, o.id)
            result[k] = o
        return result

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and starts a new session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """close the SQLAlchemy session"""
        self.__session.close()
