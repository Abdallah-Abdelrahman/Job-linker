"""Storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from server.models.base_model import Base
from server.models.user import User
from server.models.candidate import Candidate
from server.models.recruiter import Recruiter
from server.models.job import Job
from server.models.language import Language
from server.models.major import Major
from server.models.work_experience import WorkExperience
from server.models.skill import Skill

CLASSES = {
    "Candidate": Candidate,
    "Job": Job,
    "Major": Major,
    "Recruiter": Recruiter,
    "Skill": Skill,
    "User": User,
    "WorkExperience": WorkExperience,
    "Language": Language
}


class DBStorage:
    """DBStorage class

    Attributes:
        __engine: None
        __session: None


    Methods:
        __init__(self)
        reload(self)
        all(self, cls=None)
        new(self, obj)
        save(self)
        delete(self, obj=None)
    """
    __engine = None
    __session = None

    def __init__(self, engine="sqlite:///:memory:"):
        """initialize engine"""
        self.__engine = create_engine(engine, pool_pre_ping=True)
        # TODO: when testing drop tables for mysql engine

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))()

    def all(self, cls=None):
        """query on the current database session"""
        res = {}
        objs = []
        if cls:
            objs = self.__session.query(cls).all()
        else:
            for c in CLASSES:
                objs.extend(self.__session.query(c).all())

        if objs:
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                res[key] = obj
        return res

    def new(self, obj):
        """add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current db session if obj is not none"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """call remove method on the private session attribute"""
        self.__session.close()

    def drop(self, cls=None):
        """drop all tables"""
        if cls:
            self.__session.query(cls).delete()

    def rollback(self):
        """rollback all changes"""
        self.__session.rollback()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in CLASSES.values():
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
        all_class = CLASSES.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def get_user_by_email(self, email):
        """Returns the User object with the given email, None if not found."""
        User = CLASSES["User"]
        user = self.__session.query(User).filter_by(email=email).first()
        return user
