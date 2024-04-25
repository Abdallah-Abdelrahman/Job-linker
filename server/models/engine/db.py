'''Storage engine'''
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


class DBStorage:
    '''DBStorage class

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
    '''
    __engine = None
    __session = None

    def __init__(self, engine='sqlite:///:memory:'):
        '''initialize engine'''
        self.__engine = create_engine(engine, pool_pre_ping=True)
        # TODO: when testing drop tables for mysql engine

    def reload(self):
        '''create all tables in the database'''
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))()

    def all(self, cls=None):
        '''query on the current database session'''
        classes = [User, Candidate, Recruiter, Job,
                   Language, Major, WorkExperience, Skill]
        res = {}
        objs = []
        if cls:
            objs = self.__session.query(cls).all()
        else:
            for c in classes:
                objs.extend(self.__session.query(c).all())

        if objs:
            for obj in objs:
                key = f'{obj.__class__.__name__}.{obj.id}'
                res[key] = obj
        return res

    def new(self, obj):
        '''add object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from current db session if obj is not none'''
        if obj:
            self.__session.delete(obj)

    def close(self):
        '''call remove method on the private session attribute'''
        self.__session.close()

    def drop(self, cls=None):
        '''drop all tables'''
        if cls:
            self.__session.query(cls).delete()

    def rollback(self):
        '''rollback all changes'''
        self.__session.rollback()
