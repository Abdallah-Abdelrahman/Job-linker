"""
Contains the class DBStorage
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
import server.models as models
from server.models.application import Application
from server.models.base_model import Base
from server.models.candidate import Candidate
from server.models.education import Education
from server.models.job import Job
from server.models.language import Language
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
from server.models.user import User
from server.models.user_file import UserFile
from server.models.work_experience import WorkExperience

load_dotenv()


classes = {
    "Candidate": Candidate,
    "Job": Job,
    "Major": Major,
    "Recruiter": Recruiter,
    "Skill": Skill,
    "User": User,
    "WorkExperience": WorkExperience,
    "Language": Language,
    "Application": Application,
    "UserFile": UserFile,
    "Education": Education,
}


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        engine = getenv("ENGINE")
        if engine == "sqlite":
            self.__engine = create_engine(engine)
        else:
            self.__engine = create_engine(engine, pool_size=30, max_overflow=5)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def rollback(self):
        """Rollback the current transaction."""
        self.__session.rollback()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        if cls:
            return self.__session.query(cls).count()
        else:
            return sum(
                    self.__session.query(c).count() for c in classes.values()
                    )

    def get_by_attr(self, cls, attr, value):
        """
        Returns the object with the given attribute value,
        None if not found.
        """
        return self.__session.query(cls).filter(
                getattr(cls, attr) == value
                ).first()

    def get_all_by_attr(self, cls, attr, value):
        """
        Returns all objects of a class with the given attribute value.
        """
        return self.__session.query(cls).filter(
                getattr(cls, attr) == value
                ).all()
