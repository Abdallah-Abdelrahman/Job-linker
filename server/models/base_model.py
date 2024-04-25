"""BaseModel Class"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    __DATES = ("updated_at", "created_at", "start_date", "end_date")

    id = Column(
            String(60),
            primary_key=True,
            default=lambda: str(uuid.uuid4())
            )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
            )

    def __init__(self, *_, **kwargs) -> None:
        """Initialization the BaseModel instance"""
        self.id = str(uuid.uuid4())
        if isinstance(self.created_at, str):
            self.created_at = self._str_to_date(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = self._str_to_date(self.updated_at)

        if len(kwargs) == 0:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            return
        for k, v in kwargs.items():
            if k != "__class__":
                setattr(self, k, v if k not in self.__DATES
                        else self._str_to_date(v))

    def _str_to_date(self, date_str):
        """Convert a string to a datetime object"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except (ValueError, TypeError) as e:
            print("----Date issues--------->", e)
            return datetime.utcnow()

    def __repr__(self) -> str:
        """Returns a string representation of the Model instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    @property
    def to_dict(self):
        """Returns a dictionary representation of the Model instance"""
        dict_copy = self.__dict__.copy()
        dict_copy["created_at"] = self.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
                )
        dict_copy["updated_at"] = self.updated_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
                )
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy.pop("_sa_instance_state", None)
        dict_copy.pop("password", None)
        return dict_copy
